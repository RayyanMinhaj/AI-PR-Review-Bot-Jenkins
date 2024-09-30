import { Octokit } from "@octokit/rest";

const token = process.env.GITHUB_TOKEN || "";

const octokit = new Octokit({
    auth: token,
});


// this is the create function in commenter.ts line 585
export async function postComment(owner: string, repo: string, pullNumber: number, body: string) {
    try {
        await octokit.issues.createComment({
            owner,
            repo, //coderabbit is getting repo name from githubActions @actions/core, github actions workflow cannot run in parallel 
                //so we need to use environment variables here or configure the repo manually from Jenkins.
            issue_number: pullNumber,
            body,
        });
        console.log("Comment Posted Successfully"); // added for my logging
        
    } catch (error) {
        console.error("Failed to create comment");
    }
}

