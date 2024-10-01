//this is where openAI processing is taking place
import OpenAI from "openai";
import { Inputs } from "./inputs";
import { Prompts } from "./prompts";

export async function generateGPTResponse(
    title: string,
    description: string,
    fileDiff: string,
): Promise<string> {

    const openai = new OpenAI({
        apiKey: process.env.OPENAI_API_KEY, 
    });

    const inputs = new Inputs(title, description, fileDiff);

    const prompts = new Prompts();
    const summaryPrompt = prompts.renderSummarizeFileDiff(inputs, true); //gets the prompt from here

    try {
        const response = await openai.chat.completions.create({
            model: "gpt-4o-mini", // or "gpt-3.5"
            messages: [{ role: "user", content: summaryPrompt }],
        });

        // Extract and return the response text
        return response.choices[0].message?.content || "No response from OpenAI.";
    } 
    catch (error) {
        console.error("Error generating GPT response:", error);
        return "Error generating GPT response.";
    }
}
