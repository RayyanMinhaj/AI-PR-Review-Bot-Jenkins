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
      '',  // systemMessage (default value)
      prData.title,
      prData.body,
      '',  // rawSummary (default value)
      '',  // shortSummary (default value)
      '',  // filename (default value)
      'file contents cannot be provided',  // fileContent (default value)
      await this.getFileDiff(prData),  // fileDiff
      '',  // patches (default value)
      '',  // diff (default value)
      'no other comments on this patch',  // commentChain (default value)
      'no comment provided'  // comment (default value)
    );

    const summary = await this.getSummaryFromOpenAI(inputs);
    await this.postSummaryToGitHub(prData, summary);
  }

  private async getFileDiff(prData: any): Promise<string> {
    // Logic to fetch file diff will be implemented here
    return ''; // Placeholder for file diff
  }

  private async getSummaryFromOpenAI(inputs: Inputs): Promise<string> {
    // Call OpenAI API with the prompts and return the summary
    return ''; // Placeholder for summary
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
}
