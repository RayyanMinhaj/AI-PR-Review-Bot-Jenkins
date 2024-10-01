import { Octokit } from "@octokit/rest";

export async function review(owner: string, repo: string, pullNumber: number): Promise<{ title: string, description: string, fileDiff: string }> {
    const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

    const { data: pr } = await octokit.pulls.get({
        owner,
        repo,
        pull_number: pullNumber,
    });

    const { data: compare } = await octokit.repos.compareCommits({
        owner,
        repo,
        base: pr.base.sha,
        head: pr.head.sha,
    });

    const title = pr.title;
    const description = pr.body || ""; //it can be left undefined.

    // Handle the case where compare.files is undefined.
    let fileDiff = "";
    if (compare.files) {
        fileDiff = compare.files.map((file) => `${file.filename}\n${file.patch}`).join("\n\n");
    }

    console.log(fileDiff)

    return { title, description, fileDiff };
}