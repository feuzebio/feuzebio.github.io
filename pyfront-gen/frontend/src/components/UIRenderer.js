import React from 'react';
import './UIRenderer.css';

const UIRenderer = ({ analysis }) => {
    if (!analysis || !analysis.routes) {
        return null;
    }

    const renderRoute = (route) => {
        const method = route.methods[0]; // Assuming one method per route for simplicity
        switch (method) {
            case 'GET':
                return (
                    <div key={route.path} className="ui-component">
                        <h3>GET: {route.path}</h3>
                        <p>This route would display a list or a single item. A table is a good default for lists.</p>
                        <table className="ui-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Name</th>
                                    <th>Data</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>1</td>
                                    <td>Sample Item 1</td>
                                    <td>Some value</td>
                                </tr>
                                <tr>
                                    <td>2</td>
                                    <td>Sample Item 2</td>
                                    <td>Another value</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                );
            case 'POST':
                return (
                    <div key={route.path} className="ui-component">
                        <h3>POST: {route.path}</h3>
                        <p>This route creates a new resource. A form is generated based on function parameters.</p>
                        <form className="ui-form">
                            {route.params.map(param => (
                                <div className="form-group" key={param}>
                                    <label htmlFor={param}>{param}</label>
                                    <input type="text" id={param} name={param} />
                                </div>
                            ))}
                            <button type="submit">Submit</button>
                        </form>
                    </div>
                );
            case 'PUT':
                 return (
                    <div key={route.path} className="ui-component">
                        <h3>PUT: {route.path}</h3>
                        <p>This route updates a resource. A form is generated based on function parameters.</p>
                        <form className="ui-form">
                            {route.params.map(param => (
                                <div className="form-group" key={param}>
                                    <label htmlFor={param}>{param}</label>
                                    <input type="text" id={param} name={param} />
                                </div>
                            ))}
                            <button type="submit">Update</button>
                        </form>
                    </div>
                );
            case 'DELETE':
                return (
                    <div key={route.path} className="ui-component">
                        <h3>DELETE: {route.path}</h3>
                        <p>This route deletes a resource. A confirmation button is shown.</p>
                        <button className="delete-button">Delete Item</button>
                    </div>
                );
            default:
                return null;
        }
    };

    return (
        <div className="ui-renderer">
            <h2>Generated UI Preview</h2>
            {analysis.routes.map(renderRoute)}
        </div>
    );
};

export default UIRenderer;