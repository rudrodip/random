const frame = document.getElementById("frame")

frame.addEventListener("click", function (event) {
    let frameCoordinateScaled_X = event.pageX - this.offsetLeft
    let frameCoordinateScaled_Y = event.pageY - this.offsetTop

    let point = {
        x: frameCoordinateScaled_X * 2,
        y: frameCoordinateScaled_Y * 2
    }

    fetch("/", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(point)
    }).then(res => {
        console.log("Request complete! response:", res);
    });
})