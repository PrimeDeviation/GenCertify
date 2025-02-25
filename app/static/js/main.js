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
        
        // Add user message to chat
        addChatMessage('user', message);
        chatInput.value = '';
        
        try {
            const response = await fetch('/api/chat/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            
            if (response.ok) {
                const result = await response.json();
                addChatMessage('assistant', result.response);
                // Enable the evaluation section
                document.getElementById('evaluation-section').classList.remove('disabled');
            } else {
                const error = await response.json();
                addChatMessage('system', `Error: ${error.detail}`);
            }
        } catch (error) {
            addChatMessage('system', `Error: ${error.message}`);
        }
    }
    
    // Add Chat Message
    function addChatMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${role}-message`;
        
        messageDiv.innerHTML = `
            <div class="message-content">${content}</div>
            <small class="text-muted">${new Date().toLocaleTimeString()}</small>
        `;
        
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
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
}); 