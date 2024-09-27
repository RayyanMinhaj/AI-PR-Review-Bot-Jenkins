import { Prompts } from './prompts';
import { getGithubClient } from './githubClient';
import { Inputs } from './inputs';

export class ReviewBot {
  private prompts: Prompts;

  constructor() {
    this.prompts = new Prompts();
  }

  // Main function to handle the review process
  async reviewPullRequest(prData: any) {
    // Fetch the file diff for the PR
    const fileDiff = await this.getFileDiff(prData);

    // Prepare inputs for the OpenAI summary prompt
    const inputs: Inputs = new Inputs(
      'Provide a summary and inline comments based on the file diff.',
      prData.title,
      prData.body,
      '', // rawSummary (could be generated based on the PR content if needed)
      '', // shortSummary (summary of the file changes)
      '', // filename (use actual file name if needed)
      '', // fileContent (use if necessary)
      fileDiff, // fileDiff generated from getFileDiff()
      '', // patches (could be the parsed diff as patch chunks)
      '', // diff (actual difference between old and new code)
      '', // commentChain (comments related to the PR)
      ''  // comment (inline comments)
    );

    // Call OpenAI to summarize the diff
    const summary = await this.getSummaryFromOpenAI(inputs);

    // Post the summary to GitHub PR as a review comment
    await this.postSummaryToGitHub(prData, summary);

    // Post inline comments for the file diff
    await this.postInlineComments(prData, fileDiff);
  }

  private async getFileDiff(prData: any): Promise<string> {
    // Implement logic to fetch the diff of files changed in the PR
    const githubClient = getGithubClient();
    const diff = await githubClient.pulls.get({
      owner: prData.base.repo.owner.login,
      repo: prData.base.repo.name,
      pull_number: prData.number
    });
    
    // Extract and return the file diff
    return diff.data.diff_url; // or process further if necessary
  }

  private async getSummaryFromOpenAI(inputs: Inputs): Promise<string> {
    // Use the prompts class to create a summarize prompt based on inputs
    const summaryPrompt = this.prompts.renderSummarizeFileDiff(inputs, false); // false if triage is needed
    // Call OpenAI API to get the summary (assuming OpenAI integration)
    // Placeholder for OpenAI API integration
    return `Generated summary based on the following prompt: \n${summaryPrompt}`;
  }

  private async postSummaryToGitHub(prData: any, summary: string) {
    const githubClient = getGithubClient();
    await githubClient.pulls.createReview({
      owner: prData.base.repo.owner.login,
      repo: prData.base.repo.name,
      pull_number: prData.number,
      body: summary,
    });
  }

  private async postInlineComments(prData: any, fileDiff: string) {
    const githubClient = getGithubClient();

    // Process fileDiff to extract added/removed lines
    const inlineComments = this.generateInlineComments(fileDiff);

    for (const comment of inlineComments) {
      await githubClient.pulls.createReviewComment({
        owner: prData.base.repo.owner.login,
        repo: prData.base.repo.name,
        pull_number: prData.number,
        body: comment.body,
        path: comment.filePath,
        position: comment.linePosition, // Position in the diff
      });
    }
  }

  private generateInlineComments(fileDiff: string): Array<{ body: string; filePath: string; linePosition: number }> {
    const comments = [];

    // Parse the fileDiff string to identify changes
    const lines = fileDiff.split('\n');

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      // Check if the line is added or removed (e.g., starts with '+' or '-')
      if (line.startsWith('+')) {
        const commentBody = this.prompts.renderReviewFileDiff(new Inputs(
          '', '', '', '', '', 'path/to/file', '', fileDiff, '', '', ''
        ));
        comments.push({
          body: commentBody,
          filePath: 'path/to/changed/file', // Update to actual file path
          linePosition: i + 1 // Position is 1-based for GitHub comments
        });
      }
    }

    return comments;
  }
}
