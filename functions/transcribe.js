const { Configuration, OpenAIApi } = require('openai');
const multiparty = require('multiparty'); // Per gestire FormData

exports.handler = async (event) => {
  const configuration = new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
  });
  const openai = new OpenAIApi(configuration);

  try {
    // Parse FormData
    const form = new multiparty.Form();

    const formData = await new Promise((resolve, reject) => {
      form.parse(event, (err, fields, files) => {
        if (err) return reject(err);
        resolve({ fields, files });
      });
    });

    const audioFile = formData.files.file[0];

    // Call OpenAI Whisper API
    const response = await openai.createTranscription({
      file: audioFile.path,
      model: 'whisper-1',
      response_format: 'text',
    });

    // Return transcription
    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*', // CORS support
      },
      body: JSON.stringify({ transcription: response.data }),
    };
  } catch (error) {
    console.error('Error in transcription function:', error.message);

    return {
      statusCode: 500,
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify({ error: error.message }),
    };
  }
};
