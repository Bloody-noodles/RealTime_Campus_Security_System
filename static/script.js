async function updateStats(){

    const response = await fetch("/stats");

    const data = await response.json();

    document.getElementById("fps").innerHTML =
        data.fps.toFixed(1);

    document.getElementById("objects").innerHTML =
        data.objects;

    document.getElementById("person").innerHTML =
        data.counts.person || 0;

    document.getElementById("phone").innerHTML =
        data.counts.phone || 0;

    document.getElementById("laptop").innerHTML =
        data.counts.laptop || 0;

    document.getElementById("knife").innerHTML =
        data.counts.knife || 0;

    document.getElementById("gun").innerHTML =
        data.counts.gun || 0;

    document.getElementById("threat").innerHTML =
        data.threat;

}

setInterval(updateStats,500);