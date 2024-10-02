//this is called main.ts in CodeRabbit

import { postComment, postInlineComment } from "./ocktokitHelper";
import { generateGPTResponseInlineComments, generateGPTResponseMainBody } from "./bot";
import { review } from "./review";
import { splitPatch, patchStartEndLine, parsePatch, parseReviewComments, ReviewComment } from "./review";

async function run() {
    // i think it is gathering most of this data in commenter.ts and some
    // inputs from options.ts file

   const owner = process.env.GITHUB_PR_SOURCE_REPO_OWNER || ""; //RayyanMinhaj
   const repo_url = process.env.GITHUB_REPO_GIT_URL || "";
   const pullNumber = process.env.GITHUB_PR_NUMBER || "";

    //extract repo name from url (e.g., "AI-PR-Review-Bot-Jenkins")
    const repoMatch = repo_url.match(/\/([^\/]+)\.git$/);
    const repo = repoMatch ? repoMatch[1] : "";

    if (!repo) {
        console.error("Unable to determine repo name from GITHUB_REPO_GIT_URL.");
        return;
    }

    
    const { title, description, fileDiff, pullRequestSHA } = await review(owner, repo, parseInt(pullNumber)); //gets the title, description, filediff, and pullRequestSHA of PR

    //what we want to do here is that we want to run a loop for every file inside our diff, so that response is
    //generated for each file every time 
    console.log("GIT DIFF: \n", fileDiff);
    
    const fileChanges = fileDiff.split(/--- | \+\+\+/).filter(Boolean).map(file => file.trim());
    
    for (const fileContent of fileChanges){
        //the following 3 lines are done in order to extract filename for file path in inline comments
        //and content so that we can have report for EVERY FILE inside diff.
        const fileLines = fileContent.split("\n");
        const filename = fileLines[0].replace(/^--- |^\+\+\+ /, "").trim(); // Extract filename from the first line
        const content = fileLines.slice(1).join("\n"); // Get the rest of the content

        console.log("FILENAME: ", filename, "\n\n");
        console.log("CONTENT OF FILE: ", content, "\n\n\n\n");
        /////////////////////////////////////////////////////////////////////////////////////////////////
        const body = await generateGPTResponseMainBody(title, description, content); 

        await postComment(owner, repo, parseInt(pullNumber), body);

        /////////////////////////////////////////////////////////////////////////////////////////////////
        //Moving towards making inline comments
        const patches = splitPatch(fileDiff)

        for(const patch of patches){
            const hunks = parsePatch(patch)
        
            if (hunks){
                //console.log("Old Hunk: ", hunks.oldHunk); 
                //console.log("New Hunk: ", hunks.newHunk);
                const inline_comments = await generateGPTResponseInlineComments(title, description, hunks.newHunk);

                const reviewComments: ReviewComment[] = parseReviewComments(inline_comments); //this will extract all the necessary info from response



                //console.log("GPT OPENAI REVIEW COMMENTS: ", inline_comments);
                //console.log("REVIEW COMMENTS INTERFACE: ", reviewComments);
            

                await postInlineComment(owner, repo, parseInt(pullNumber), pullRequestSHA, filename, reviewComments);


            }

        }

    }
    





}

run();