const leftBtn = document.getElementById('leftBtn');
const rightBtn = document.getElementById('rightBtn');
const listItems = document.querySelectorAll('.list-item');
const imageContainer = document.getElementById('imageContainer');
const descriptionContainer = document.getElementById('descriptionContainer').getElementsByTagName('ul')[0];

let currentIndex = 0;

const images = [
    "https://via.placeholder.com/400",
    "https://via.placeholder.com/400/FF0000",
    "https://via.placeholder.com/400/00FF00",
    "https://via.placeholder.com/400/0000FF"
];

const descriptions = [
    ["Description for Element 1 - Item 1", "Description for Element 1 - Item 2"],
    ["Description for Element 2 - Item 1", "Description for Element 2 - Item 2"],
    ["Description for Element 3 - Item 1", "Description for Element 3 - Item 2"],
    ["Description for Element 4 - Item 1", "Description for Element 4 - Item 2"]
];

function updateActiveItem(index) {
    listItems.forEach((item, i) => {
        item.classList.toggle('active', i === index);
    });
    updateImageAndDescription(index);
}

function updateImageAndDescription(index) {
    imageContainer.innerHTML = `<img src="${images[index]}" alt="Image for Element ${index + 1}">`;
    descriptionContainer.innerHTML = descriptions[index].map(desc => `<li>${desc}</li>`).join('');
}

leftBtn.addEventListener('click', () => {
    currentIndex = (currentIndex > 0) ? currentIndex - 1 : listItems.length - 1;
    updateActiveItem(currentIndex);
});

rightBtn.addEventListener('click', () => {
    currentIndex = (currentIndex < listItems.length - 1) ? currentIndex + 1 : 0;
    updateActiveItem(currentIndex);
});

updateActiveItem(currentIndex); // Initialize first item as active

window.onload = (e) => {

}
