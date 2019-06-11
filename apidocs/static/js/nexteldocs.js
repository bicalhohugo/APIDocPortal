function buildSwaggerUI(url) {
    // Build a system
    const ui = SwaggerUIBundle({
        url: url,
        validatorUrl : null,
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
            SwaggerUIBundle.presets.apis,
            SwaggerUIStandalonePreset.slice(1)
        ],
        plugins: [
            SwaggerUIBundle.plugins.DownloadUrl
        ],
        layout: "StandaloneLayout"
    });

    return ui;
}