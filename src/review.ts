// review.ts

import { Octokit } from "@octokit/rest";
import { generateGPTResponse } from "./bot";
import { postComment } from "./ocktokitHelper";

const token = process.env.GITHUB_TOKEN || "";
const openaiApiKey = process.env.OPENAI_API_KEY || "";

const octokit = new Octokit({
  auth: token,
});

async function run() {
  const owner = process.env.GITHUB_PR_SOURCE_REPO_OWNER || "";
  const repoUrl = process.env.GITHUB_REPO_GIT_URL || "";
  const pullNumber = process.env.GITHUB_PR_NUMBER || "";

  // Extract repo name from url
  const repoMatch = repoUrl.match(/\/([^\/]+)\.git$/);
  const repo = repoMatch ? repoMatch[1] : "";

  if (!repo) {
    console.error(
      "Unable to determine repo name from GITHUB_REPO_GIT_URL."
    );
    return;
  }

  // Get the base and head commits from the pull request
  const { data: pullRequest } = await octokit.pulls.get({
    owner,
    repo,
    pull_number: parseInt(pullNumber),
  });

  const baseCommit = pullRequest.base.sha;
  const headCommit = pullRequest.head.sha;

  // Get the diff between the base and head commits (using logic from review.ts - line 110)
  const { data: diff } = await octokit.repos.compareCommits({
    owner,
    repo,
    base: baseCommit,
    head: headCommit,
  });

  // Generate the review response using OpenAI
  const reviewResponse = await generateGPTResponse(
    pullRequest.title,
    pullRequest.body,
    diff.files.map((file) => file.patch).join("\n"),
    "" // You can add a short summary here if needed
  );

  // Post the review comment
  await postComment(owner, repo, parseInt(pullNumber), reviewResponse);
}

run();