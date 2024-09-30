import { postComment } from "./ocktokitHelper";

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

    const body = "THIS IS A TEST COMMENT FROM AI BOT!!!!!!!";

    await postComment(owner, repo, parseInt(pullNumber), body);

    
}

run();