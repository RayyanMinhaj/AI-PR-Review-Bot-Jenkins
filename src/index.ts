import { ReviewBot } from './reviewBot';

const reviewBot = new ReviewBot();

async function run() {
  const prData = JSON.parse(process.env.PR_DATA || '{}'); 
  await reviewBot.reviewPullRequest(prData);
}

run().catch(console.error);
