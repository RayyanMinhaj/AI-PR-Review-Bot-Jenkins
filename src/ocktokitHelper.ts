//this is a mix of the octokit.ts and commenter.ts file

import { Octokit } from "@octokit/rest";
import { ReviewComment } from "./review";


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


//////////////////////////////////////////////////////////////////////////////////


export async function postInlineComment(owner: string, repo:string, pullNumber: number, pullRequestSHA: string, filename:string, reviewComments:ReviewComment[])
{
    for(const comment of reviewComments){
        console.log("\n\nHeres the comment to be posted brah: ",comment.comment, "\n");
        if (!comment.comment.includes("LGTM!")){
            try{
                comment.lineTo = comment.lineTo -1;
                await octokit.pulls.createReviewComment({
                    owner: owner,
                    repo: repo,
                    pull_number: pullNumber,
                    commit_id: pullRequestSHA, 
                    body: comment.comment,
                    path: filename,
                    line: comment.lineTo,
                    side: 'RIGHT',
                });
    
                console.log(`Comment posted on lines ${comment.lineFrom}-${comment.lineTo}: ${comment.comment}`);
        
            }
            catch(error){
                console.error(`Error posting comment on lines ${comment.lineFrom}-${comment.lineTo}:`, error);
            }
        }
        
    }

}