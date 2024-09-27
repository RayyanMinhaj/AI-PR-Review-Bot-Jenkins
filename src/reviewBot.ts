import { Prompts } from './prompts';
import { getGithubClient } from './githubClient';
import { Inputs } from './inputs';

export class ReviewBot {
  private prompts: Prompts;

  constructor() {
    this.prompts = new Prompts();
  }

  async reviewPullRequest(prData: any) {
    const inputs: Inputs = new Inputs(
      'Provide a summary and inline comments based on the file diff.',
      prData.title,
      prData.body,
      '', // rawSummary
      '', // shortSummary
      '', // filename (you can fetch the filename from the PR data)
      '', // fileContent (if applicable)
      await this.getFileDiff(prData), // fileDiff
      '', // patches (if applicable)
      '', // diff (if applicable)
      '', // commentChain
      ''  // comment
    );

    const summary = await this.getSummaryFromOpenAI(inputs);
    await this.postSummaryToGitHub(prData, summary);

    const fileDiff = inputs.fileDiff;
    await this.postInlineComments(prData, fileDiff);
  }

  private async getFileDiff(prData: any): Promise<string> {
    // Implement logic to fetch the diff of files changed in the PR
    return ''; // Placeholder
  }

  private async getSummaryFromOpenAI(inputs: Inputs): Promise<string> {
    // Call OpenAI API with the prompts and return the summary
    return ''; // Placeholder
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
        const commentBody = this.generateCommentForLine(line);
        comments.push({
          body: commentBody,
          filePath: 'path/to/changed/file', // Update to actual file path
          linePosition: i + 1 // Position is 1-based for GitHub comments
        });
      }
    }
    
    return comments;
  }

  private generateCommentForLine(line: string): string {
    
    return `This line adds functionality: ${line.trim()}`; // Placeholder
  }
}
