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

    console.log("GIT DIFF: ", fileDiff);

    /////////////////////////////////////////////////////////////////////////////////////////////////
    const body = await generateGPTResponseMainBody(title, description, fileDiff); 

    await postComment(owner, repo, parseInt(pullNumber), body);

    /////////////////////////////////////////////////////////////////////////////////////////////////
    //Moving towards making inline comments
    const patches = splitPatch(fileDiff)

    for(const patch of patches){
        const hunks = parsePatch(patch)
    
        if (hunks){
            console.log("Old Hunk: ", hunks.oldHunk); 
            console.log("New Hunk: ", hunks.newHunk);
            const inline_comments = await generateGPTResponseInlineComments(title, description, hunks.newHunk);

            const reviewComments: ReviewComment[] = parseReviewComments(inline_comments); //this will extract all the necessary info from response



            console.log("GPT OPENAI REVIEW COMMENTS: ", inline_comments);
            console.log("REVIEW COMMENTS INTERFACE: ", reviewComments);
        

            await postInlineComment(owner, repo, parseInt(pullNumber), pullRequestSHA, reviewComments);



        }

    }



}

run();