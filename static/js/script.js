// ==========================================
// DASHBOARD UPDATE
// ==========================================

async function refreshDashboard() {

    try {

        const response = await fetch("/api/dashboard");

        const data = await response.json();

        // ==================================
        // COUNTS
        // ==================================

        document.getElementById("person").innerHTML =
            data.counts.person;

        document.getElementById("phone").innerHTML =
            data.counts.phone;

        document.getElementById("bottle").innerHTML =
            data.counts.bottle;

        document.getElementById("knife").innerHTML =
            data.counts.knife;

        document.getElementById("gun").innerHTML =
            data.counts.gun;

        document.getElementById("fps").innerHTML =
            Number(data.fps).toFixed(1);

        // ==================================
        // SYSTEM STATUS
        // ==================================

        const status =
            document.getElementById("status");

        if(data.danger){

            status.innerHTML =
                "🔴 THREAT DETECTED";

            status.className =
                "danger";

        }

        else{

            status.innerHTML =
                "🟢 SYSTEM SAFE";

            status.className =
                "safe";

        }

        // ==================================
        // RECENT DETECTIONS
        // ==================================

        const tbody =
            document.querySelector("#history tbody");

        tbody.innerHTML = "";

                data.logs.forEach(log => {

            tbody.innerHTML += `

                <tr>

                    <td>${log.object_name}</td>

                    <td>${(Number(log.confidence) * 100).toFixed(1)}%</td>

                    <td>${log.timestamp}</td>

                </tr>

            `;

        });

        // ============================
        // INCIDENT TIMELINE
        // ============================

                        const timeline = document.getElementById("timeline");

                timeline.innerHTML = "";

                data.timeline.forEach(event=>{

                timeline.innerHTML += `

                <div class="timeline-item">

                <div class="timeline-time">

                ${event.time}

                </div>

                <div class="timeline-title">

                ${event.icon} ${event.title}

                </div>

                <div class="timeline-desc">

                ${event.description}

                </div>

                </div>

                `;

                });

        // ==================================
        // LATEST SCREENSHOT
        // ==================================

        const image =
            document.getElementById("latestCapture");

        if(data.latest_capture){

            image.src =
                "/captures/" +
                data.latest_capture +
                "?t=" +
                new Date().getTime();

        }

    }

    catch(error){

        console.log(error);

    }

}

// ==========================================
// START
// ==========================================

refreshDashboard();

setInterval(

    refreshDashboard,

    1000

);