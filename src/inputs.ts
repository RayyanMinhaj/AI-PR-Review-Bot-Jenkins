// inputs.ts - but shortened from CodeRabbits repo

export class Inputs {
    title: string;
    description: string;
    fileDiff: string;
    patches: string;
    shortSummary: string;
  
    constructor(
      title = 'no title provided',
      description = 'no description provided',
      fileDiff = 'file diff cannot be provided',
      shortSummary = 'no summary provided',
      patches = ''
    ) {
      this.title = title;
      this.description = description;
      this.fileDiff = fileDiff;
      this.shortSummary = shortSummary;
      this.patches = patches
    }
  
    render(content: string): string {
      if (!content) {
        return '';
      }
      if (this.title) {
        content = content.replace('$title', this.title);
      }
      if (this.description) {
        content = content.replace('$description', this.description);
      }
      if (this.fileDiff) {
        content = content.replace('$file_diff', this.fileDiff);
      }
      if (this.shortSummary) {
        content = content.replace('$short_summary', this.shortSummary);
      }
      if (this.patches) {
        content = content.replace('$patches', this.patches)
      }
      return content;
    }
  }
  