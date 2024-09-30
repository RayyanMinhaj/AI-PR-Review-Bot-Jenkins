//this is called main.ts in CodeRabbit

import { postComment } from "./ocktokitHelper";
import { generateGPTResponse } from "./bot";
import { review } from "./review";

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

    /////////THIS NEEDS TO BE REPLACED WITH THE REAL STUFF///////////////////
    //const title = "Example PR Title";                                   ///
    //const description = "This is an example description for the PR.";   ///
    //const fileDiff = "Here would be the diff output...";                ///
    /////////////////////////////////////////////////////////////////////////

    const { title, description, fileDiff } = await review(owner, repo, parseInt(pullNumber));

    const body = await generateGPTResponse(title, description, fileDiff);

    await postComment(owner, repo, parseInt(pullNumber), body);

}

run();