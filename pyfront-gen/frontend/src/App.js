import React, { useState } from 'react';
import axios from 'axios';
import Editor from 'react-simple-code-editor';
import { highlight, languages } from 'prismjs/components/prism-core';
import 'prismjs/components/prism-python';
import 'prismjs/themes/prism.css'; //Example style, you can use another
import './App.css';
import UIRenderer from './components/UIRenderer';
import { generateHtml, generateCss, generateJs } from './logic/CodeGenerator';

const initialCode = `from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def get_users():
    """Returns a list of users."""
    return jsonify([{'id': 1, 'name': 'John Doe'}, {'id': 2, 'name': 'Jane Doe'}])

@app.route('/api/users', methods=['POST'])
def create_user():
    """Creates a new user."""
    # In a real app, you'd get data from request.json
    return jsonify({'status': 'User created'}), 201
`;

function App() {
    const [code, setCode] = useState(initialCode);
    const [analysis, setAnalysis] = useState(null);
    const [error, setError] = useState('');

    const handleExport = async () => {
        if (!analysis) {
            setError('Nenhuma análise para exportar. Por favor, analise o código primeiro.');
            return;
        }

        try {
            const html = generateHtml(analysis);
            const css = generateCss();
            const js = generateJs();

            const response = await axios.post('http://localhost:5001/api/export', {
                html,
                css,
                js
            }, {
                responseType: 'blob', // Important to handle the zip file
            });

            // Create a link and trigger the download
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'frontend.zip');
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);

        } catch (err) {
            setError('Falha ao exportar o código.');
            console.error(err);
        }
    };

    const handleAnalyze = async () => {
        try {
            setError('');
            setAnalysis(null);
            const response = await axios.post('http://localhost:5001/api/analyze', { code });
            if (response.data.error) {
                setError(response.data.error);
            } else {
                setAnalysis(response.data);
            }
        } catch (err) {
            setError('Failed to connect to the analysis server.');
            console.error(err);
        }
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>PyFront-Gen</h1>
                <p>Cole seu código Python (Flask/FastAPI) abaixo para gerar um front-end básico.</p>
            </header>
            <main>
                <div className="code-editor-container">
                    <Editor
                        value={code}
                        onValueChange={code => setCode(code)}
                        highlight={code => highlight(code, languages.python)}
                        padding={10}
                        style={{
                            fontFamily: '"Fira code", "Fira Mono", monospace',
                            fontSize: 14,
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                        }}
                    />
                </div>
                <div className="action-buttons">
                    <button onClick={handleAnalyze} className="analyze-button">
                        Analisar e Gerar Front-end
                    </button>
                    <button onClick={handleExport} className="export-button" disabled={!analysis}>
                        Exportar Código
                    </button>
                </div>
                {error && <div className="error-message">{error}</div>}
                <div className="split-screen">
                    <div className="preview-panel">
                        {analysis ? (
                            <UIRenderer analysis={analysis} />
                        ) : (
                            <div className="placeholder">
                                O preview da UI gerada aparecerá aqui.
                            </div>
                        )}
                    </div>
                    <div className="editor-panel">
                        {/* Visual editor and code tabs will go here */}
                         <div className="placeholder">
                                O painel de edição aparecerá aqui.
                         </div>
                    </div>
                </div>
            </main>
        </div>
    );
}

export default App;