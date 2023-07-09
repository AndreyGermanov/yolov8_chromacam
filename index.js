document.addEventListener("DOMContentLoaded", () => {
    const img = document.querySelector("img");
    // Update video frame image each 30 milliseconds
    setInterval(()=> {
        img.src = "./frame.jpg?t="+(new Date()).getTime();
    },30);

    // Set event handlers for controls
    document.getElementById("change_background").addEventListener("click", change_background);
    document.getElementById("blur").addEventListener("change",set_blur);
    document.getElementById("reset").addEventListener("click",reset);
})

// Function used to upload an image to the backend
// that will be used as a background
function change_background(event) {
    const input = document.createElement("input");
    input.setAttribute("type", "file");
    input.style.display = 'none';
    input.click();
    document.body.appendChild(input);
    input.addEventListener("change", async (event) => {
        const file = event.target.files[0];
        const form = new FormData();
        form.append("background", file);
        await fetch("/background", {
            method: "POST",
            body: form
        })
        document.body.removeChild(input);

    })
}

// Function used to set background blur level on the backend
function set_blur(event) {
    fetch("/blur/"+event.target.value);
}

// Function used to send reset request to the backend
// to remove blur and background
function reset() {
    fetch("/reset");
    document.getElementById("blur").value = 0;
}

