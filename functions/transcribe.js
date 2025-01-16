const { Configuration, OpenAIApi } = require("openai");

exports.handler = async (event) => {
  const configuration = new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
  });
  const openai = new OpenAIApi(configuration);

  const audioBuffer = Buffer.from(event.body, 'base64');
  
  try {
    const response = await openai.createTranscription({
      file: audioBuffer,
      model: "whisper-1",
      response_format: "text",
    });

    return {
      statusCode: 200,
      body: JSON.stringify({ transcription: response.data }),
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message }),
    };
  }
};
