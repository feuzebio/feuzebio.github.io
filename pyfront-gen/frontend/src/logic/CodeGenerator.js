const generateHtml = (analysis) => {
    let bodyContent = '';

    analysis.routes.forEach(route => {
        const method = route.methods[0].toUpperCase();
        if (method === 'GET') {
            bodyContent += `
                <div class="component">
                    <h2>${route.path} (GET)</h2>
                    <p>Sample table for GET request.</p>
                    <table>
                        <thead><tr><th>ID</th><th>Name</th></tr></thead>
                        <tbody><tr><td>1</td><td>Example</td></tr></tbody>
                    </table>
                </div>
            `;
        } else if (method === 'POST') {
            const formFields = route.params.map(param => `
                <div class="form-group">
                    <label for="${param}">${param}</label>
                    <input type="text" id="${param}" name="${param}">
                </div>
            `).join('');
            bodyContent += `
                <div class="component">
                    <h2>${route.path} (POST)</h2>
                    <form>
                        ${formFields}
                        <button type="submit">Submit</button>
                    </form>
                </div>
            `;
        }
    });

    return `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Generated Frontend</title>
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
            <header>
                <h1>Generated UI</h1>
            </header>
            <main>
                ${bodyContent}
            </main>
            <script src="script.js"></script>
        </body>
        </html>
    `;
};

const generateCss = () => {
    return `
        body { font-family: sans-serif; background-color: #f4f4f4; color: #333; }
        header { background-color: #333; color: white; padding: 1rem; text-align: center; }
        main { max-width: 800px; margin: 2rem auto; padding: 1rem; }
        .component { background: white; border: 1px solid #ddd; padding: 1.5rem; margin-bottom: 1.5rem; border-radius: 5px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ccc; padding: 0.8rem; text-align: left; }
        th { background-color: #f2f2f2; }
        form { display: flex; flex-direction: column; gap: 1rem; }
        .form-group { display: flex; flex-direction: column; }
        label { margin-bottom: 0.5rem; font-weight: bold; }
        input { padding: 0.5rem; border: 1px solid #ccc; border-radius: 3px; }
        button { background-color: #28a745; color: white; padding: 0.7rem 1.5rem; border: none; border-radius: 3px; cursor: pointer; }
        button:hover { background-color: #218838; }
    `;
};

const generateJs = () => {
    return `
        document.addEventListener('DOMContentLoaded', () => {
            console.log('Generated JavaScript loaded.');
            // Add interactivity here in the future
        });
    `;
};

export { generateHtml, generateCss, generateJs };