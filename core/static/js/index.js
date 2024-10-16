

let fileList = [];
let currentContourLayer = null; // Store reference to the current GeoJSON layer
const map = L.map('map').setView([23.6850, 90.3563], 7); // Centered on Bangladesh

function updateInputFileHint() {
    const layer = document.getElementById('input-layer').value;
    const hintElement = document.getElementById('file-hint');

    switch (layer) {
        case 'contour':
            hintElement.innerText = 'Please upload a GeoJSON file for Contour.';
            break;
        case 'topography':
            hintElement.innerText = 'Please upload a GeoTIFF or GeoJSON file for Topography.';
            break;
        case 'ecozone':
            hintElement.innerText = 'Please upload a GeoJSON file for EcoZone.';
            break;
        case 'administrative_boundary':
            hintElement.innerText = 'Please upload a GeoJSON file for Administrative Boundary.';
            break;
        case 'infrastructure':
            hintElement.innerText = 'Please upload a CSV or GeoJSON file for Infrastructure.';
            break;
        case 'socioeconomic':
            hintElement.innerText = 'Please upload a CSV or GeoJSON file for Socioeconomic data.';
            break;
        case 'digital_grid':
            hintElement.innerText = 'Please upload a GeoJSON file for Digital Grid.';
            break;
        case 'temporal_evolution':
            hintElement.innerText = 'Please upload a CSV or GeoJSON file for Temporal Evolution.';
            break;
        default:
            hintElement.innerText = '';
            break;
    }
}

function addFileToList() {
    const layer_field = document.getElementById('input-layer');
    const layer = layer_field.value;
    const fileInput = document.getElementById('geojson-file');
    const file = fileInput.files[0];
    const selectedLayer = layer_field.options[layer_field.selectedIndex];

    if (!layer || !file) {
        alert('Please select both an input layer and a file.');
        return;
    }

    // Add the file to the list
    fileList.push({ layer: layer, file: file });
    selectedLayer.disabled = true;
    layer_field.selectedIndex = 0;

    // Reset file input for further selections
    fileInput.value = '';

    renderFileList();
    if (layer === "contour") loadContour(file);
}

function toTitleCase(str) {
    return str
        .replace(/_/g, ' ') // Replace underscores with spaces
        .toLowerCase() // Convert the whole string to lowercase first
        .split(' ') // Split the string by spaces into an array of words
        .map(word => word.charAt(0).toUpperCase() + word.slice(1)) // Capitalize the first letter of each word
        .join(' '); // Join the array back into a string
}

function renderFileList() {
    const list = document.getElementById('file-list');
    list.innerHTML = ''; // Clear existing list items

    fileList.forEach((item, index) => {
        const listItem = document.createElement('li');
        listItem.classList.add('file-item');
        listItem.innerHTML = `
            <div class="file-info">
                <label>${toTitleCase(item.layer)}</label>
                <span class="file-name">${item.file.name.length > 20 ? item.file.name.slice(0, 17) + '...' : item.file.name}</span>
            </div>
            <div class="file-actions">
                <button type="button" onclick="changeFile(${index})">Change</button>
                <button type="button" onclick="removeFile(${index})">Remove</button>
            </div>
        `;
        list.appendChild(listItem);
    });
}

function changeFile(index) {
    const newFileInput = document.createElement('input');
    newFileInput.type = 'file';
    newFileInput.accept = '.json, .geojson, .csv';
    newFileInput.onchange = () => {
        const newFile = newFileInput.files[0];
        if (newFile) {
            fileList[index].file = newFile;
            renderFileList();
            if (fileList[index].layer === "contour") {
                loadContour(newFile);
            }
        }
    };
    newFileInput.click();
}

function removeFile(index) {
    console.log(fileList[index]);
    const inputOption = document.getElementById("option_" + fileList[index].layer);
    inputOption.disabled = false;
    fileList.splice(index, 1);
    renderFileList();
}

function loadContour(contour_file) {
    // Add a basic OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    if (contour_file && contour_file.name.endsWith(".geojson")) {
        const reader = new FileReader();

        reader.onload = function (e) {
            const geoJsonData = JSON.parse(e.target.result);

            // Remove old contour layer if it exists
            if (currentContourLayer) {
                map.removeLayer(currentContourLayer);
            }

            currentContourLayer = L.geoJSON(geoJsonData, {
                style: function (feature) {
                    return {
                        color: "#FF7800",
                        weight: 2,
                        opacity: 1,
                    }
                },
                onEachFeature: function (feature, layer) {
                    // Check if the feature has a name property
                    if (feature.properties && feature.properties.name) {
                        layer.bindPopup(feature.properties.name); // Show name in a popup
                        // Or use bindTooltip for a tooltip instead
                        // layer.bindTooltip(feature.properties.name);
                    }
                },
            }).addTo(map);

            const bounds = currentContourLayer.getBounds();
            map.fitBounds(bounds);
        };

        reader.readAsText(contour_file);
    }
}

function loadInputLayersStatus() {
    fetch(getAvailableInputsURL, {
        method: "GET",
    }).then(response => {
        return response.json();
    }).then(data => {
        data.layers.forEach((layer, idx) => {
            const layerStatus = document.getElementById(layer + "_status")

            if (layerStatus !== null) {
                layerStatus.classList.add("available")
            }
        })
    })
}

// Override form submission to send files manually via JavaScript
// Override form submission to send files manually via JavaScript
document.getElementById('input-form').onsubmit = function (event) {
    event.preventDefault(); // Prevent default form submission

    const formData = new FormData();

    fileList.forEach(item => {
        formData.append(item.layer, item.file);
    });

    // Now submit formData using fetch or XMLHttpRequest
    fetch(uploadGeojsonURL, {
        method: 'POST',
        body: formData,
        headers: {
            // 'X-CSRFToken': '{{ csrf_token }}' // Include CSRF token in the request
        }
    }).then(response => {
        if (response.ok) {
            alert('Files uploaded successfully');
            loadInputLayersStatus();
        } else {
            console.log(response)
            alert('Failed to upload files');
        }
    }).catch(error => {
        alert('Error: ' + error.message);
    });
};

window.onload = () => {
    loadContour(null);
    loadInputLayersStatus();
}
