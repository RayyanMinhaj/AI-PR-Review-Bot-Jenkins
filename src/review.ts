import { Octokit } from "@octokit/rest";

export async function review(owner: string, repo: string, pullNumber: number): Promise<{ title: string, description: string, fileDiff: string, pullRequestSHA: string }> {
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
    const pullRequestSHA = pr.head.sha;

    // Handle the case where compare.files is undefined.
    let fileDiff = "";
    if (compare.files) {
        fileDiff = compare.files.map((file) => 
            `--- ${file.filename}\n+++ ${file.filename}\n${file.patch}`
        ).join("\n\n");
    }


    //console.log(fileDiff)

    return { title, description, fileDiff, pullRequestSHA };
}


//////////////////////////// Following section deals with inline commenting ///////////////////////////////

//most of this logic is taken from reviews.ts (line: 809 - parsePatch function)
export interface HunkInfo {
  oldHunk: { startLine: number; endLine: number };
  newHunk: { startLine: number; endLine: number };
}

export const splitPatch = async (patch: string | null | undefined): Promise<string[]> => {
  if (patch == null) {
    return [];
  }

  const pattern = /(^@@ -(\d+),(\d+) \+(\d+),(\d+) @@).*$/gm;

  const result: string[] = [];
  let last = -1;
  let match: RegExpExecArray | null;
  while ((match = pattern.exec(patch)) !== null) {
    if (last === -1) {
      last = match.index;
    } else {
      result.push(patch.substring(last, match.index));
      last = match.index;
    }
  }
  if (last !== -1) {
    result.push(patch.substring(last));
  }
  return result;
};

export const patchStartEndLine = async (
  patch: string
): Promise<HunkInfo | null> => {
  const pattern = /(^@@ -(\d+),(\d+) \+(\d+),(\d+) @@)/gm;
  const match = pattern.exec(patch);
  if (match != null) {
    const oldBegin = parseInt(match[2]);
    const oldDiff = parseInt(match[3]);
    const newBegin = parseInt(match[4]);
    const newDiff = parseInt(match[5]);
    return {
      oldHunk: {
        startLine: oldBegin,
        endLine: oldBegin + oldDiff - 1,
      },
      newHunk: {
        startLine: newBegin,
        endLine: newBegin + newDiff - 1,
      },
    };
  } else {
    return null;
  }
};

export const parsePatch = async (
  patch: string
): Promise<{ oldHunk: string; newHunk: string } | null> => {
  const hunkInfo = await patchStartEndLine(patch);
  if (hunkInfo == null) {
    return null;
  }

  const oldHunkLines: string[] = [];
  const newHunkLines: string[] = [];

  let newLine = hunkInfo.newHunk.startLine;

  const lines = patch.split('\n').slice(1); // Skip the @@ line

  if (lines[lines.length - 1] === '') {
    lines.pop();
  }

  // Skip annotations for the first 3 and last 3 lines
  const skipStart = 3;
  const skipEnd = 3;

  let currentLine = 0;

  // Flag to identify if there are only removals in the patch
  const removalOnly = !lines.some((line) => line.startsWith('+'));

  for (const line of lines) {
    currentLine++;
    if (line.startsWith('-')) {
      oldHunkLines.push(`${line.substring(1)}`);
    } else if (line.startsWith('+')) {
      newHunkLines.push(`${newLine}: ${line.substring(1)}`);
      newLine++;
    } else {
      // context line
      oldHunkLines.push(`${line}`);
      if (
        removalOnly ||
        (currentLine > skipStart && currentLine <= lines.length - skipEnd)
      ) {
        newHunkLines.push(`${newLine}: ${line}`);
      } else {
        newHunkLines.push(`${line}`);
      }
      newLine++;
    }
  }

  return {
    oldHunk: oldHunkLines.join('\n'),
    newHunk: newHunkLines.join('\n'),
  };
};


///This is to parse the gpt response and extract line to, line from, and the inline comment////
export interface ReviewComment {
  lineFrom: number;
  lineTo: number;
  comment: string;
}

export async function parseReviewComments(text: string): Promise<ReviewComment[]> {
  const reviewComments: ReviewComment[] = [];
  const lines = text.split("\n");

  let lineFrom: number | null = null;
  let lineTo: number | null = null;
  let commentLines: string[] = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();

    const lineMatch = line.match(/^Lines (\d+)-(\d+):$/);
    if (lineMatch) {
      // If we have a previous comment, save it
      if (lineFrom !== null && lineTo !== null && commentLines.length > 0) {
        reviewComments.push({
          lineFrom,
          lineTo,
          comment: commentLines.join("\n").trim(),
        });
        commentLines = [];
      }

      // Extract new line numbers
      lineFrom = parseInt(lineMatch[1], 10);
      lineTo = parseInt(lineMatch[2], 10);
    } else if (line.startsWith("Lines ")) {
      
      const singleLineMatch = line.match(/^Lines (\d+):$/);
      if (singleLineMatch) {
        if (lineFrom !== null && lineTo !== null && commentLines.length > 0) {
          reviewComments.push({
            lineFrom,
            lineTo,
            comment: commentLines.join("\n").trim(),
          });
          commentLines = [];
        }

        lineFrom = parseInt(singleLineMatch[1], 10);
        lineTo = lineFrom;
      }
    } else if (line) {
      
      commentLines.push(line);
    }
  }

  if (lineFrom !== null && lineTo !== null && commentLines.length > 0) {
    reviewComments.push({
      lineFrom,
      lineTo,
      comment: commentLines.join("\n").trim(),
    });
  }

  return reviewComments;
}
