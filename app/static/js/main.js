// DOM Elements
document.addEventListener('DOMContentLoaded', function() {
    // Organization Form
    const orgForm = document.getElementById('organization-form');
    const orgNameInput = document.getElementById('org-name');
    const orgIndustrySelect = document.getElementById('org-industry');
    const orgSizeSelect = document.getElementById('org-size');
    
    // Certification Selection
    const certificationSelect = document.getElementById('certification-select');
    
    // Document Upload
    const documentUploadForm = document.getElementById('document-upload-form');
    const documentFileInput = document.getElementById('document-file');
    const documentTypeSelect = document.getElementById('document-type');
    const uploadedDocumentsList = document.getElementById('uploaded-documents');
    
    // Chat Interface
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatContainer = document.getElementById('chat-container');
    
    // Evaluation
    const evaluationForm = document.getElementById('evaluation-form');
    const evaluationProgress = document.getElementById('evaluation-progress');
    const evaluationProgressBar = document.getElementById('evaluation-progress-bar');
    
    // Results
    const resultsContainer = document.getElementById('results-container');
    const documentGenerationForm = document.getElementById('document-generation-form');
    
    // Help Modal
    const helpBtn = document.getElementById('help-btn');
    
    // Integration Elements
    const googleIntegrationSwitch = document.getElementById('google-integration');
    const msIntegrationSwitch = document.getElementById('microsoft-integration');
    const githubIntegrationSwitch = document.getElementById('github-integration');
    
    const connectGoogleBtn = document.getElementById('configure-google');
    const disconnectGoogleBtn = document.getElementById('disconnect-google');
    const connectMicrosoftBtn = document.getElementById('connect-microsoft');
    const connectGithubBtn = document.getElementById('connect-github');
    
    // Navigation Elements
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.content-section');
    const chatMessages = document.getElementById('chat-messages');
    const currentSectionLabel = document.getElementById('current-section');
    
    // Theme Toggle
    const themeToggle = document.getElementById('theme-toggle');
    
    // Event Listeners
    if (orgForm) {
        orgForm.addEventListener('submit', handleOrganizationSubmit);
    }
    
    if (documentUploadForm) {
        documentUploadForm.addEventListener('submit', handleDocumentUpload);
    }
    
    if (chatForm) {
        chatForm.addEventListener('submit', handleChatSubmit);
    }
    
    if (evaluationForm) {
        evaluationForm.addEventListener('submit', handleEvaluationSubmit);
    }
    
    if (documentGenerationForm) {
        documentGenerationForm.addEventListener('submit', handleDocumentGeneration);
    }
    
    // Add event listeners for integration buttons
    if (connectGoogleBtn) {
        connectGoogleBtn.addEventListener('click', configureGoogleIntegration);
    }
    
    if (disconnectGoogleBtn) {
        disconnectGoogleBtn.addEventListener('click', disconnectGoogleIntegration);
    }
    
    if (connectMicrosoftBtn) {
        connectMicrosoftBtn.addEventListener('click', connectMicrosoftIntegration);
    }
    
    if (connectGithubBtn) {
        connectGithubBtn.addEventListener('click', connectGithubIntegration);
    }
    
    // Integration toggle switches
    if (googleIntegrationSwitch) {
        googleIntegrationSwitch.addEventListener('change', function() {
            const googleIntegrationElements = document.querySelectorAll('#google-docs-integration, #google-drive-integration, #google-folder-id, #browse-google-folders, #google-read-permission, #google-write-permission');
            
            googleIntegrationElements.forEach(element => {
                element.disabled = !this.checked;
            });
            
            if (!this.checked) {
                showAlert('Google integration disabled. Your connection settings have been preserved.', 'info');
            } else {
                showAlert('Google integration enabled.', 'success');
            }
        });
    }
    
    if (msIntegrationSwitch) {
        msIntegrationSwitch.addEventListener('change', function() {
            const msIntegrationElements = document.querySelectorAll('#ms-office-integration, #onedrive-integration, #ms-folder-path, #browse-ms-folders, #ms-read-permission, #ms-write-permission');
            
            if (this.checked) {
                // If enabling, don't enable elements yet - wait for connection
                connectMicrosoftBtn.classList.remove('d-none');
                showAlert('Please connect your Microsoft 365 account to enable integration.', 'info');
            } else {
                // If disabling, disable all elements
                msIntegrationElements.forEach(element => {
                    element.disabled = true;
                });
                connectMicrosoftBtn.classList.add('d-none');
                showAlert('Microsoft 365 integration disabled.', 'info');
            }
        });
    }
    
    if (githubIntegrationSwitch) {
        githubIntegrationSwitch.addEventListener('change', function() {
            const githubIntegrationElements = document.querySelectorAll('#github-repo, #github-branch, #create-github-branch, #github-repo-permission, #github-workflow-permission, #github-auto-commit');
            
            if (this.checked) {
                // If enabling, don't enable elements yet - wait for connection
                connectGithubBtn.classList.remove('d-none');
                showAlert('Please connect your GitHub account to enable integration.', 'info');
            } else {
                // If disabling, disable all elements
                githubIntegrationElements.forEach(element => {
                    element.disabled = true;
                });
                connectGithubBtn.classList.add('d-none');
                showAlert('GitHub integration disabled.', 'info');
            }
        });
    }
    
    // Add event listeners for navigation
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Get the target section ID from the href attribute
            const targetId = this.getAttribute('href').substring(1);
            
            // Update active nav link
            navLinks.forEach(navLink => navLink.classList.remove('active'));
            this.classList.add('active');
            
            // Hide all sections and show the target section
            sections.forEach(section => section.classList.add('d-none'));
            document.getElementById(targetId).classList.remove('d-none');
            
            // Update current section label for chat
            if (currentSectionLabel) {
                currentSectionLabel.textContent = this.textContent.trim();
            }
            
            // Clear chat messages when switching sections
            if (chatMessages) {
                chatMessages.innerHTML = '';
                
                // Add a welcome message for the new section
                const welcomeMessage = document.createElement('div');
                welcomeMessage.className = 'chat-message system-message';
                welcomeMessage.innerHTML = `
                    <div class="message-content">
                        <p>You are now in the <strong>${this.textContent.trim()}</strong> section. How can I help you with this section?</p>
                    </div>
                `;
                chatMessages.appendChild(welcomeMessage);
                
                // Scroll to the bottom of the chat
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        });
    });
    
    // Add event listener for theme toggle
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            // Update theme
            document.documentElement.setAttribute('data-bs-theme', newTheme);
            
            // Update toggle icon
            this.innerHTML = newTheme === 'dark' ? 
                '<i class="fas fa-sun"></i>' : 
                '<i class="fas fa-moon"></i>';
            
            // Save preference
            localStorage.setItem('theme', newTheme);
            
            // Show feedback
            showAlert(`Theme switched to ${newTheme} mode`, 'info');
        });
    }
    
    // Add event listeners for settings save
    const aiModelSelect = document.getElementById('ai-model');
    const temperatureRange = document.getElementById('temperature-range');
    const saveSettingsBtn = document.getElementById('save-settings');
    
    if (aiModelSelect) {
        aiModelSelect.addEventListener('change', function() {
            localStorage.setItem('aiModel', this.value);
        });
    }
    
    if (temperatureRange) {
        temperatureRange.addEventListener('input', function() {
            const tempValue = document.getElementById('temperature-value');
            if (tempValue) {
                tempValue.textContent = this.value;
            }
            localStorage.setItem('temperature', this.value);
        });
    }
    
    if (saveSettingsBtn) {
        saveSettingsBtn.addEventListener('click', function() {
            // Get all settings values
            const aiModel = document.getElementById('ai-model').value;
            const temperature = document.getElementById('temperature-range').value;
            
            // Save to localStorage
            localStorage.setItem('aiModel', aiModel);
            localStorage.setItem('temperature', temperature);
            
            // Additional settings from other tabs
            const username = document.getElementById('username')?.value;
            const email = document.getElementById('email')?.value;
            
            if (username) localStorage.setItem('username', username);
            if (email) localStorage.setItem('email', email);
            
            // Show success message
            showAlert('Settings saved successfully!', 'success');
        });
    }
    
    // Organization Form Handler
    async function handleOrganizationSubmit(e) {
        e.preventDefault();
        
        const orgData = {
            name: orgNameInput.value,
            industry: orgIndustrySelect.value,
            size: orgSizeSelect.value
        };
        
        try {
            const response = await fetch('/api/organizations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(orgData)
            });
            
            if (response.ok) {
                const result = await response.json();
                showAlert('Organization information saved successfully!', 'success');
                // Enable the next section
                document.getElementById('certification-section').classList.remove('disabled');
            } else {
                const error = await response.json();
                showAlert(`Error: ${error.detail}`, 'danger');
            }
        } catch (error) {
            showAlert(`Error: ${error.message}`, 'danger');
        }
    }
    
    // Document Upload Handler
    async function handleDocumentUpload(e) {
        e.preventDefault();
        
        const formData = new FormData();
        formData.append('file', documentFileInput.files[0]);
        formData.append('document_type', documentTypeSelect.value);
        
        try {
            const response = await fetch('/api/documents/upload', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const result = await response.json();
                showAlert('Document uploaded successfully!', 'success');
                addDocumentToList(result.document_id, documentTypeSelect.value, documentFileInput.files[0].name);
                documentFileInput.value = '';
                // Enable the chat section
                document.getElementById('chat-section').classList.remove('disabled');
            } else {
                const error = await response.json();
                showAlert(`Error: ${error.detail}`, 'danger');
            }
        } catch (error) {
            showAlert(`Error: ${error.message}`, 'danger');
        }
    }
    
    // Add Document to List
    function addDocumentToList(id, type, filename) {
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item d-flex justify-content-between align-items-center';
        listItem.innerHTML = `
            <div>
                <span class="badge bg-primary me-2">${type}</span>
                ${filename}
            </div>
            <button class="btn btn-sm btn-danger delete-doc" data-id="${id}">
                <i class="fas fa-trash"></i>
            </button>
        `;
        
        listItem.querySelector('.delete-doc').addEventListener('click', async function() {
            try {
                const response = await fetch(`/api/documents/${id}`, {
                    method: 'DELETE'
                });
                
                if (response.ok) {
                    listItem.remove();
                    showAlert('Document deleted successfully!', 'success');
                } else {
                    const error = await response.json();
                    showAlert(`Error: ${error.detail}`, 'danger');
                }
            } catch (error) {
                showAlert(`Error: ${error.message}`, 'danger');
            }
        });
        
        uploadedDocumentsList.appendChild(listItem);
    }
    
    // Chat Submit Handler
    async function handleChatSubmit(e) {
        e.preventDefault();
        
        const message = chatInput.value.trim();
        if (!message) return;
        
        // Get current active section
        const activeSection = document.querySelector('.content-section:not(.d-none)');
        const sectionId = activeSection ? activeSection.id : null;
        const sectionName = document.querySelector('.nav-link.active') ? 
                           document.querySelector('.nav-link.active').textContent.trim() : 
                           'General';
        
        // Add user message to chat
        addMessageToChat('user', message);
        
        // Clear input
        chatInput.value = '';
        
        try {
            // Show typing indicator
            const typingIndicator = document.createElement('div');
            typingIndicator.className = 'chat-message system-message typing-indicator';
            typingIndicator.innerHTML = '<div class="message-content"><p>AI is typing...</p></div>';
            chatMessages.appendChild(typingIndicator);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            // Get selected model from settings
            const selectedModel = document.getElementById('ai-model') ? 
                                 document.getElementById('ai-model').value : 
                                 'gpt-4o';
            
            // In a real app, you would send the message to your backend API
            // For demo purposes, we'll simulate a response
            const context = {
                section: sectionId,
                sectionName: sectionName,
                model: selectedModel
            };
            
            console.log('Sending chat message with context:', context);
            
            // Simulate API delay
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            // Remove typing indicator
            document.querySelector('.typing-indicator').remove();
            
            // Generate a contextual response based on the current section
            let response;
            switch(sectionId) {
                case 'organization-section':
                    response = "I can help you with your organization details. You can provide information about your company structure, policies, and compliance requirements here.";
                    break;
                case 'documents-section':
                    response = "This is where you can upload and manage your compliance documents. What type of documents would you like to work with?";
                    break;
                case 'certifications-section':
                    response = "I can assist with certification requirements. Would you like information about specific compliance frameworks like ISO 27001, SOC 2, or GDPR?";
                    break;
                case 'evaluation-section':
                    response = "In the evaluation section, we can assess your current compliance status against selected frameworks. Would you like to start an evaluation?";
                    break;
                case 'results-section':
                    response = "Here you can review your compliance results and generated documents. Is there a specific report you'd like to analyze?";
                    break;
                case 'settings-section':
                    response = "I can help you configure your settings. Would you like assistance with AI model configuration, integrations, or account settings?";
                    break;
                default:
                    response = "I'm here to help with your compliance needs. What would you like to know about GenCertify?";
            }
            
            // Add AI response to chat
            addMessageToChat('ai', response);
            
        } catch (error) {
            console.error('Error sending message:', error);
            
            // Remove typing indicator if it exists
            const typingIndicator = document.querySelector('.typing-indicator');
            if (typingIndicator) {
                typingIndicator.remove();
            }
            
            // Show error message
            addMessageToChat('system', 'Sorry, there was an error processing your request. Please try again.');
        }
    }
    
    // Add message to chat
    function addMessageToChat(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.className = `chat-message ${sender}-message`;
        
        let avatar = '';
        let name = '';
        
        switch(sender) {
            case 'user':
                avatar = '<div class="avatar"><i class="fas fa-user"></i></div>';
                name = 'You';
                break;
            case 'ai':
                avatar = '<div class="avatar"><i class="fas fa-robot"></i></div>';
                name = 'AI Assistant';
                break;
            case 'system':
                avatar = '<div class="avatar"><i class="fas fa-info-circle"></i></div>';
                name = 'System';
                break;
        }
        
        messageElement.innerHTML = `
            ${avatar}
            <div class="message-content">
                <div class="message-header">
                    <span class="message-sender">${name}</span>
                    <span class="message-time">${new Date().toLocaleTimeString()}</span>
                </div>
                <p>${message}</p>
            </div>
        `;
        
        chatMessages.appendChild(messageElement);
        
        // Scroll to the bottom of the chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Evaluation Submit Handler
    async function handleEvaluationSubmit(e) {
        e.preventDefault();
        
        const selectedCertifications = Array.from(certificationSelect.selectedOptions).map(option => option.value);
        
        if (selectedCertifications.length === 0) {
            showAlert('Please select at least one certification to evaluate.', 'warning');
            return;
        }
        
        try {
            // Create evaluation
            const createResponse = await fetch('/api/evaluations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ certification_types: selectedCertifications })
            });
            
            if (!createResponse.ok) {
                const error = await createResponse.json();
                showAlert(`Error: ${error.detail}`, 'danger');
                return;
            }
            
            const { evaluation_id } = await createResponse.json();
            
            // Start evaluation
            const startResponse = await fetch(`/api/evaluations/${evaluation_id}/run`, {
                method: 'POST'
            });
            
            if (!startResponse.ok) {
                const error = await startResponse.json();
                showAlert(`Error: ${error.detail}`, 'danger');
                return;
            }
            
            // Show progress
            evaluationProgress.classList.remove('d-none');
            
            // Poll for status
            const statusInterval = setInterval(async () => {
                try {
                    const statusResponse = await fetch(`/api/evaluations/${evaluation_id}/status`);
                    
                    if (statusResponse.ok) {
                        const status = await statusResponse.json();
                        
                        // Update progress bar
                        evaluationProgressBar.style.width = `${status.progress}%`;
                        evaluationProgressBar.setAttribute('aria-valuenow', status.progress);
                        evaluationProgressBar.textContent = `${status.progress}%`;
                        
                        if (status.status === 'completed') {
                            clearInterval(statusInterval);
                            showAlert('Evaluation completed successfully!', 'success');
                            
                            // Get results
                            const resultsResponse = await fetch(`/api/evaluations/${evaluation_id}/results`);
                            
                            if (resultsResponse.ok) {
                                const results = await resultsResponse.json();
                                displayResults(results);
                                // Enable the results section
                                document.getElementById('results-section').classList.remove('disabled');
                            }
                        } else if (status.status === 'failed') {
                            clearInterval(statusInterval);
                            showAlert('Evaluation failed. Please try again.', 'danger');
                        }
                    }
                } catch (error) {
                    clearInterval(statusInterval);
                    showAlert(`Error: ${error.message}`, 'danger');
                }
            }, 2000);
        } catch (error) {
            showAlert(`Error: ${error.message}`, 'danger');
        }
    }
    
    // Display Results
    function displayResults(results) {
        resultsContainer.innerHTML = '';
        
        results.certifications.forEach(cert => {
            const certCard = document.createElement('div');
            certCard.className = 'card mb-3';
            
            const statusClass = cert.readiness_level === 'High' ? 'success' : 
                               cert.readiness_level === 'Medium' ? 'warning' : 'danger';
            
            certCard.innerHTML = `
                <div class="card-header bg-${statusClass} text-white">
                    <h5 class="mb-0">${cert.certification_type}</h5>
                </div>
                <div class="card-body">
                    <h6>Readiness Level: <span class="badge bg-${statusClass}">${cert.readiness_level}</span></h6>
                    <p>${cert.summary}</p>
                    <h6>Recommendations:</h6>
                    <ul class="list-group list-group-flush mb-3">
                        ${cert.recommendations.map(rec => `<li class="list-group-item">${rec}</li>`).join('')}
                    </ul>
                </div>
            `;
            
            resultsContainer.appendChild(certCard);
        });
    }
    
    // Document Generation Handler
    async function handleDocumentGeneration(e) {
        e.preventDefault();
        
        const selectedDocTypes = Array.from(
            document.querySelectorAll('input[name="document-types"]:checked')
        ).map(checkbox => checkbox.value);
        
        if (selectedDocTypes.length === 0) {
            showAlert('Please select at least one document type to generate.', 'warning');
            return;
        }
        
        try {
            // Get the latest evaluation ID
            const evaluationsResponse = await fetch('/api/evaluations');
            
            if (!evaluationsResponse.ok) {
                const error = await evaluationsResponse.json();
                showAlert(`Error: ${error.detail}`, 'danger');
                return;
            }
            
            const evaluations = await evaluationsResponse.json();
            const latestEvaluation = evaluations[0]?.evaluation_id;
            
            if (!latestEvaluation) {
                showAlert('No evaluation found. Please run an evaluation first.', 'warning');
                return;
            }
            
            // Create document generation
            const createResponse = await fetch('/api/documents/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    evaluation_id: latestEvaluation,
                    document_types: selectedDocTypes
                })
            });
            
            if (!createResponse.ok) {
                const error = await createResponse.json();
                showAlert(`Error: ${error.detail}`, 'danger');
                return;
            }
            
            const { document_generation_id } = await createResponse.json();
            
            showAlert('Document generation started. You will be notified when documents are ready.', 'info');
            
            // Poll for status
            const statusInterval = setInterval(async () => {
                try {
                    const statusResponse = await fetch(`/api/documents/generate/${document_generation_id}/status`);
                    
                    if (statusResponse.ok) {
                        const status = await statusResponse.json();
                        
                        if (status.status === 'completed') {
                            clearInterval(statusInterval);
                            showAlert('Documents generated successfully!', 'success');
                            
                            // Get document list
                            const documentsResponse = await fetch('/api/documents');
                            
                            if (documentsResponse.ok) {
                                const documents = await documentsResponse.json();
                                displayGeneratedDocuments(documents);
                            }
                        } else if (status.status === 'failed') {
                            clearInterval(statusInterval);
                            showAlert('Document generation failed. Please try again.', 'danger');
                        }
                    }
                } catch (error) {
                    clearInterval(statusInterval);
                    showAlert(`Error: ${error.message}`, 'danger');
                }
            }, 2000);
        } catch (error) {
            showAlert(`Error: ${error.message}`, 'danger');
        }
    }
    
    // Display Generated Documents
    function displayGeneratedDocuments(documents) {
        const generatedDocsList = document.getElementById('generated-documents');
        generatedDocsList.innerHTML = '';
        
        documents.forEach(doc => {
            const listItem = document.createElement('li');
            listItem.className = 'list-group-item d-flex justify-content-between align-items-center';
            listItem.innerHTML = `
                <div>
                    <span class="badge bg-success me-2">${doc.document_type}</span>
                    ${doc.filename}
                </div>
                <a href="${doc.download_url}" class="btn btn-sm btn-primary" target="_blank">
                    <i class="fas fa-download"></i> Download
                </a>
            `;
            
            generatedDocsList.appendChild(listItem);
        });
    }
    
    // Show Alert
    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.role = 'alert';
        
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        document.querySelector('.alert-container').appendChild(alertDiv);
        
        // Auto dismiss after 5 seconds
        setTimeout(() => {
            alertDiv.classList.remove('show');
            setTimeout(() => alertDiv.remove(), 150);
        }, 5000);
    }
    
    // Google Integration Functions
    async function configureGoogleIntegration() {
        try {
            // Get current settings
            const googleDocsEnabled = document.getElementById('google-docs-integration').checked;
            const googleDriveEnabled = document.getElementById('google-drive-integration').checked;
            const folderId = document.getElementById('google-folder-id').value;
            const readPermission = document.getElementById('google-read-permission').checked;
            const writePermission = document.getElementById('google-write-permission').checked;
            
            // Validate settings
            if (!googleDocsEnabled && !googleDriveEnabled) {
                showAlert('Please enable at least one Google service.', 'warning');
                return;
            }
            
            if (!readPermission && !writePermission) {
                showAlert('Please select at least one permission.', 'warning');
                return;
            }
            
            // Save settings
            const settings = {
                docs_enabled: googleDocsEnabled,
                drive_enabled: googleDriveEnabled,
                folder_id: folderId,
                read_permission: readPermission,
                write_permission: writePermission
            };
            
            // In a real app, you would send these settings to the server
            console.log('Google integration settings:', settings);
            
            // Show success message
            showAlert('Google integration settings saved successfully!', 'success');
        } catch (error) {
            showAlert(`Error: ${error.message}`, 'danger');
        }
    }
    
    async function disconnectGoogleIntegration() {
        if (confirm('Are you sure you want to disconnect Google integration? This will revoke access to your Google account.')) {
            try {
                // In a real app, you would send a request to the server to revoke the OAuth token
                
                // Update UI
                document.getElementById('google-integration').checked = false;
                
                const googleIntegrationElements = document.querySelectorAll('#google-docs-integration, #google-drive-integration, #google-folder-id, #browse-google-folders, #google-read-permission, #google-write-permission');
                
                googleIntegrationElements.forEach(element => {
                    element.disabled = true;
                });
                
                // Show success message
                showAlert('Google integration disconnected successfully.', 'success');
            } catch (error) {
                showAlert(`Error: ${error.message}`, 'danger');
            }
        }
    }
    
    // Microsoft 365 Integration Functions
    async function connectMicrosoftIntegration() {
        try {
            // In a real app, this would redirect to Microsoft OAuth flow
            // For demo purposes, we'll simulate a successful connection
            
            // Open OAuth popup
            const width = 600;
            const height = 600;
            const left = (window.innerWidth - width) / 2;
            const top = (window.innerHeight - height) / 2;
            
            // Simulate OAuth flow with a timeout
            showAlert('Connecting to Microsoft 365...', 'info');
            
            setTimeout(() => {
                // Update UI to show connected state
                const msIntegrationElements = document.querySelectorAll('#ms-office-integration, #onedrive-integration, #ms-folder-path, #browse-ms-folders, #ms-read-permission, #ms-write-permission');
                
                msIntegrationElements.forEach(element => {
                    element.disabled = false;
                });
                
                // Enable checkboxes by default
                document.getElementById('ms-office-integration').checked = true;
                document.getElementById('onedrive-integration').checked = true;
                document.getElementById('ms-read-permission').checked = true;
                document.getElementById('ms-write-permission').checked = true;
                
                // Update connection status
                const statusBadge = connectMicrosoftBtn.closest('.card-body').querySelector('.badge');
                statusBadge.textContent = 'Connected';
                statusBadge.classList.remove('bg-secondary');
                statusBadge.classList.add('bg-success');
                
                // Add connected account info
                const statusDiv = connectMicrosoftBtn.closest('.card-body').querySelector('div:first-child');
                const accountInfo = document.createElement('small');
                accountInfo.className = 'text-muted ms-2';
                accountInfo.textContent = 'Connected as john.doe@example.com';
                statusDiv.appendChild(accountInfo);
                
                // Change button to configure/disconnect
                connectMicrosoftBtn.innerHTML = '<i class="fas fa-cog me-1"></i> Configure';
                connectMicrosoftBtn.classList.remove('btn-primary');
                connectMicrosoftBtn.classList.add('btn-outline-secondary');
                
                const disconnectBtn = document.createElement('button');
                disconnectBtn.className = 'btn btn-sm btn-outline-danger ms-2';
                disconnectBtn.innerHTML = '<i class="fas fa-unlink me-1"></i> Disconnect';
                disconnectBtn.addEventListener('click', disconnectMicrosoftIntegration);
                
                connectMicrosoftBtn.parentNode.appendChild(disconnectBtn);
                
                showAlert('Microsoft 365 connected successfully!', 'success');
            }, 2000);
        } catch (error) {
            showAlert(`Error: ${error.message}`, 'danger');
        }
    }
    
    async function disconnectMicrosoftIntegration() {
        if (confirm('Are you sure you want to disconnect Microsoft 365 integration? This will revoke access to your Microsoft account.')) {
            try {
                // In a real app, you would send a request to the server to revoke the OAuth token
                
                // Update UI
                document.getElementById('microsoft-integration').checked = false;
                
                const msIntegrationElements = document.querySelectorAll('#ms-office-integration, #onedrive-integration, #ms-folder-path, #browse-ms-folders, #ms-read-permission, #ms-write-permission');
                
                msIntegrationElements.forEach(element => {
                    element.disabled = true;
                    if (element.type === 'checkbox') {
                        element.checked = false;
                    }
                });
                
                // Reset connection status
                const statusBadge = document.querySelector('#microsoft-integration').closest('.card').querySelector('.badge');
                statusBadge.textContent = 'Not Connected';
                statusBadge.classList.remove('bg-success');
                statusBadge.classList.add('bg-secondary');
                
                // Remove account info
                const statusDiv = document.querySelector('#microsoft-integration').closest('.card').querySelector('.card-body div:first-child');
                const accountInfo = statusDiv.querySelector('small');
                if (accountInfo) {
                    accountInfo.remove();
                }
                
                // Reset buttons
                const buttonsDiv = document.querySelector('#microsoft-integration').closest('.card').querySelector('.card-body div:last-child');
                buttonsDiv.innerHTML = `
                    <button class="btn btn-sm btn-primary" id="connect-microsoft">
                        <i class="fas fa-plug me-1"></i> Connect with Microsoft
                    </button>
                `;
                
                document.getElementById('connect-microsoft').addEventListener('click', connectMicrosoftIntegration);
                
                // Show success message
                showAlert('Microsoft 365 integration disconnected successfully.', 'success');
            } catch (error) {
                showAlert(`Error: ${error.message}`, 'danger');
            }
        }
    }
    
    // GitHub Integration Functions
    async function connectGithubIntegration() {
        try {
            // In a real app, this would redirect to GitHub OAuth flow
            // For demo purposes, we'll simulate a successful connection
            
            // Open OAuth popup
            const width = 600;
            const height = 600;
            const left = (window.innerWidth - width) / 2;
            const top = (window.innerHeight - height) / 2;
            
            // Simulate OAuth flow with a timeout
            showAlert('Connecting to GitHub...', 'info');
            
            setTimeout(() => {
                // Update UI to show connected state
                const githubIntegrationElements = document.querySelectorAll('#github-repo, #github-branch, #create-github-branch, #github-repo-permission, #github-workflow-permission, #github-auto-commit');
                
                githubIntegrationElements.forEach(element => {
                    element.disabled = false;
                });
                
                // Enable checkboxes by default
                document.getElementById('github-repo-permission').checked = true;
                document.getElementById('github-workflow-permission').checked = true;
                document.getElementById('github-auto-commit').checked = true;
                
                // Populate repository dropdown
                const repoSelect = document.getElementById('github-repo');
                repoSelect.innerHTML = '';
                
                const repos = [
                    { id: 'new', name: '+ Create new repository' },
                    { id: 'user/compliance-docs', name: 'user/compliance-docs' },
                    { id: 'user/security-policies', name: 'user/security-policies' },
                    { id: 'organization/iso27001', name: 'organization/iso27001' }
                ];
                
                repos.forEach(repo => {
                    const option = document.createElement('option');
                    option.value = repo.id;
                    option.textContent = repo.name;
                    repoSelect.appendChild(option);
                });
                
                // Update connection status
                const statusBadge = connectGithubBtn.closest('.card-body').querySelector('.badge');
                statusBadge.textContent = 'Connected';
                statusBadge.classList.remove('bg-secondary');
                statusBadge.classList.add('bg-success');
                
                // Add connected account info
                const statusDiv = connectGithubBtn.closest('.card-body').querySelector('div:first-child');
                const accountInfo = document.createElement('small');
                accountInfo.className = 'text-muted ms-2';
                accountInfo.textContent = 'Connected as github-user';
                statusDiv.appendChild(accountInfo);
                
                // Change button to configure/disconnect
                connectGithubBtn.innerHTML = '<i class="fas fa-cog me-1"></i> Configure';
                connectGithubBtn.classList.remove('btn-dark');
                connectGithubBtn.classList.add('btn-outline-secondary');
                
                const disconnectBtn = document.createElement('button');
                disconnectBtn.className = 'btn btn-sm btn-outline-danger ms-2';
                disconnectBtn.innerHTML = '<i class="fas fa-unlink me-1"></i> Disconnect';
                disconnectBtn.addEventListener('click', disconnectGithubIntegration);
                
                connectGithubBtn.parentNode.appendChild(disconnectBtn);
                
                showAlert('GitHub connected successfully!', 'success');
            }, 2000);
        } catch (error) {
            showAlert(`Error: ${error.message}`, 'danger');
        }
    }
    
    async function disconnectGithubIntegration() {
        if (confirm('Are you sure you want to disconnect GitHub integration? This will revoke access to your GitHub account.')) {
            try {
                // In a real app, you would send a request to the server to revoke the OAuth token
                
                // Update UI
                document.getElementById('github-integration').checked = false;
                
                const githubIntegrationElements = document.querySelectorAll('#github-repo, #github-branch, #create-github-branch, #github-repo-permission, #github-workflow-permission, #github-auto-commit');
                
                githubIntegrationElements.forEach(element => {
                    element.disabled = true;
                    if (element.type === 'checkbox') {
                        element.checked = false;
                    }
                });
                
                // Reset repository dropdown
                const repoSelect = document.getElementById('github-repo');
                repoSelect.innerHTML = '<option value="" selected disabled>Select a repository</option>';
                
                // Reset connection status
                const statusBadge = document.querySelector('#github-integration').closest('.card').querySelector('.badge');
                statusBadge.textContent = 'Not Connected';
                statusBadge.classList.remove('bg-success');
                statusBadge.classList.add('bg-secondary');
                
                // Remove account info
                const statusDiv = document.querySelector('#github-integration').closest('.card').querySelector('.card-body div:first-child');
                const accountInfo = statusDiv.querySelector('small');
                if (accountInfo) {
                    accountInfo.remove();
                }
                
                // Reset buttons
                const buttonsDiv = document.querySelector('#github-integration').closest('.card').querySelector('.card-body div:last-child');
                buttonsDiv.innerHTML = `
                    <button class="btn btn-sm btn-dark" id="connect-github">
                        <i class="fas fa-plug me-1"></i> Connect with GitHub
                    </button>
                `;
                
                document.getElementById('connect-github').addEventListener('click', connectGithubIntegration);
                
                // Show success message
                showAlert('GitHub integration disconnected successfully.', 'success');
            } catch (error) {
                showAlert(`Error: ${error.message}`, 'danger');
            }
        }
    }
    
    // Initialize the app
    function initApp() {
        // Set the first nav link as active by default
        if (navLinks.length > 0) {
            navLinks[0].click();
        }
        
        // Initialize theme from localStorage
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-bs-theme', savedTheme);
        
        // Update theme toggle button icon
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.innerHTML = savedTheme === 'dark' ? 
                '<i class="fas fa-sun"></i>' : 
                '<i class="fas fa-moon"></i>';
        }
        
        // Initialize AI model from localStorage
        const savedModel = localStorage.getItem('aiModel');
        const modelSelect = document.getElementById('ai-model');
        if (savedModel && modelSelect) {
            modelSelect.value = savedModel;
        }
        
        // Initialize temperature from localStorage
        const savedTemp = localStorage.getItem('temperature');
        const tempRange = document.getElementById('temperature-range');
        const tempValue = document.getElementById('temperature-value');
        if (savedTemp && tempRange && tempValue) {
            tempRange.value = savedTemp;
            tempValue.textContent = savedTemp;
        }
    }
    
    // Call initApp on page load
    initApp();
}); 