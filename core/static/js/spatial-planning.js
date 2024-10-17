const leftBtn = document.getElementById('leftBtn');
const rightBtn = document.getElementById('rightBtn');
const divisionContainer = document.getElementById("divisionContainer")
const divisionSliderItems = document.getElementsByClassName('division-slider-item');
const imageContainer = document.getElementById('imageContainer');
const descriptionContainer = document.getElementById('descriptionContainer');

let currentIndex = 0;

const spatialPlanImages = [];

const spatialPlanLandUseData = [];

function updateActiveItem(index) {
    Object.entries(divisionSliderItems).forEach(([_, item], i) => {
        item.classList.toggle('active', i === index);
    });
    updateImageAndDescription(index);
}

function updateImageAndDescription(index) {
    imageContainer.innerHTML = `<img src="${spatialPlanImages[index]}" alt="Image for Element ${index + 1}">`;

    descriptionContainer.innerHTML = ""

    const descHeader = document.createElement("h2");
    descHeader.innerHTML = divisionSliderItems[index].innerHTML

    const descList = document.createElement("ul");

    Object.entries(spatialPlanLandUseData[index]).forEach(([category, area]) => {
        if (category === "public_space") {
            const descSubList = document.createElement("ul");

            Object.entries(area).forEach(([subCategory, subArea]) => {
               const subItem = document.createElement("li");
               subItem.innerHTML = toTitleCase(subCategory) + ": " + subArea + " sq. k.m."

                descSubList.appendChild(subItem);
            });

            descList.appendChild(descSubList);
        } else {
            const descItem = document.createElement("li");
            descItem.innerHTML = toTitleCase(category) + ": " + area + " sq. k.m."

            descList.appendChild(descItem)
        }
    })

    descriptionContainer.appendChild(descHeader);
    descriptionContainer.appendChild(descList);
}

function toTitleCase(str) {
    return str
        .replace(/_/g, ' ') // Replace underscores with spaces
        .toLowerCase() // Convert the whole string to lowercase first
        .split(' ') // Split the string by spaces into an array of words
        .map(word => word.charAt(0).toUpperCase() + word.slice(1)) // Capitalize the first letter of each word
        .join(' '); // Join the array back into a string
}

leftBtn.addEventListener('click', () => {
    currentIndex = (currentIndex > 0) ? currentIndex - 1 : divisionSliderItems.length - 1;
    updateActiveItem(currentIndex);
});

rightBtn.addEventListener('click', () => {
    currentIndex = (currentIndex < divisionSliderItems.length - 1) ? currentIndex + 1 : 0;
    updateActiveItem(currentIndex);
});

// updateActiveItem(currentIndex); // Initialize first item as active

window.onload = (e) => {
    fetch(getSpatialPlanningURL, {
        method: "GET",
    }).then(response => {
        return response.json();
    }).then(data => {
        Object.entries(data.spatial_plan_images).forEach(([division, image]) => {
            spatialPlanImages.push(image)
            const divisionSliderItem = document.createElement("div");
            divisionSliderItem.classList.add("division-slider-item");
            divisionSliderItem.innerHTML = division;

            divisionContainer.appendChild(divisionSliderItem);
            // divisionSliderItems.push(divisionSliderItem);

        });

        Object.entries(data.land_use).forEach(([division, land_use]) => {
            spatialPlanLandUseData.push(land_use);

        });

        updateActiveItem(currentIndex);
        if (spatialPlanImages.length > 0) {
            document.getElementById("cursorButtons").style.visibility = "visible";
        }

    }).catch(error => {
        window.location.href = "/";
    });
}
