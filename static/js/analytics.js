// ======================================
// ANALYTICS.JS
// ======================================

// ---------- CLOCK ----------

function updateClock() {

    const now = new Date();

    document.getElementById("clock").innerText =
        now.toLocaleTimeString();

}

updateClock();

setInterval(updateClock, 1000);


// ======================================
// BAR CHART
// ======================================

const barCtx = document.getElementById("barChart").getContext("2d");

const barChart = new Chart(barCtx, {

    type: "bar",

    data: {

        labels: [

            "Person",

            "Phone",

            "Laptop",

            "Bottle",

            "Knife",

            "Gun"

        ],

        datasets: [

            {

                label: "Detections",

                data: [0,0,0,0,0,0],

                backgroundColor: [

                    "#2ecc71",

                    "#3498db",

                    "#9b59b6",

                    "#f1c40f",

                    "#e67e22",

                    "#e74c3c"

                ],

                borderRadius:8

            }

        ]

    },

    options: {

        responsive:true,

        maintainAspectRatio:false,

        plugins:{

            legend:{

                display:false

            }

        },

        scales:{

            y:{

                beginAtZero:true

            }

        }

    }

});


// ======================================
// PIE CHART
// ======================================

const pieCtx = document.getElementById("pieChart").getContext("2d");

const pieChart = new Chart(pieCtx,{

    type:"pie",

    data:{

        labels:[

            "Person",

            "Phone",

            "Laptop",

            "Bottle",

            "Knife",

            "Gun"

        ],

        datasets:[{

            data:[0,0,0,0,0,0],

            backgroundColor:[

                "#2ecc71",

                "#3498db",

                "#9b59b6",

                "#f1c40f",

                "#e67e22",

                "#e74c3c"

            ]

        }]

    },

    options:{

        responsive:true,

        maintainAspectRatio:false

    }

});


// ======================================
// LINE CHART
// ======================================

const lineCtx = document.getElementById("lineChart").getContext("2d");

const lineChart = new Chart(lineCtx,{

    type:"line",

    data:{

        labels:[],

        datasets:[{

            label:"Objects",

            data:[],

            borderColor:"#00c3ff",

            backgroundColor:"rgba(0,195,255,.15)",

            fill:true,

            tension:.4

        }]

    },

    options:{

        responsive:true,

        maintainAspectRatio:false

    }

});

// ======================================
// FETCH DASHBOARD DATA
// ======================================

async function refreshAnalytics(){

    try{

        const response = await fetch("/api/dashboard");

        const data = await response.json();

        // ==================================
        // SUMMARY CARDS
        // ==================================

        document.getElementById("analyticsPersons").innerText =
            data.counts.person;

        document.getElementById("analyticsPhones").innerText =
            data.counts.phone;

        document.getElementById("analyticsLaptops").innerText =
            data.counts.laptop;

        document.getElementById("analyticsWeapons").innerText =
            data.counts.gun + data.counts.knife;

        // ==================================
        // SECURITY SUMMARY
        // ==================================

        const totalObjects =

            data.counts.person +

            data.counts.phone +

            data.counts.laptop +

            data.counts.bottle +

            data.counts.knife +

            data.counts.gun;

        document.getElementById("totalObjects").innerText =
            totalObjects;

        document.getElementById("averageFPS").innerText =
            Number(data.fps).toFixed(1);

        document.getElementById("capturedThreats").innerText =
            data.counts.gun + data.counts.knife;

        if(data.danger){

            document.getElementById("threatLevel").innerText =
                "HIGH";

            document.getElementById("systemStatus").innerText =
                "THREAT";

            document.getElementById("systemStatus").style.color =
                "#ff4444";

        }

        else{

            document.getElementById("threatLevel").innerText =
                "LOW";

            document.getElementById("systemStatus").innerText =
                "SAFE";

            document.getElementById("systemStatus").style.color =
                "#00ff66";

        }

        // ==================================
        // FIND MOST DETECTED OBJECT
        // ==================================

        let topName = "";

        let topCount = -1;

        Object.entries(data.counts).forEach(([name,count])=>{

            if(count > topCount){

                topCount = count;

                topName = name;

            }

        });

        document.getElementById("topObject").innerText =
            topName.toUpperCase();

        // ==================================
        // HIGHEST CONFIDENCE
        // ==================================

        let highest = 0;

        let lastTime = "--";

        data.logs.forEach(log=>{

            if(log.confidence > highest){

                highest = log.confidence;

            }

            if(lastTime === "--"){

                lastTime = log.timestamp;

            }

        });

        document.getElementById("highestConfidence").innerText =
            (highest * 100).toFixed(1) + "%";

        document.getElementById("lastDetection").innerText =
            lastTime;
                    // ==================================
        // UPDATE BAR CHART
        // ==================================

        const chartData = [

            data.counts.person,

            data.counts.phone,

            data.counts.laptop,

            data.counts.bottle,

            data.counts.knife,

            data.counts.gun

        ];

        barChart.data.datasets[0].data = chartData;

        barChart.update();

        // ==================================
        // UPDATE PIE CHART
        // ==================================

        pieChart.data.datasets[0].data = chartData;

        pieChart.update();

        // ==================================
        // UPDATE LINE CHART
        // ==================================

        const now = new Date();

        const currentTime = now.toLocaleTimeString();

        lineChart.data.labels.push(currentTime);

        lineChart.data.datasets[0].data.push(totalObjects);

        if(lineChart.data.labels.length > 10){

            lineChart.data.labels.shift();

            lineChart.data.datasets[0].data.shift();

        }

        lineChart.update();

        // ==================================
        // HISTORY TABLE
        // ==================================

        const tbody = document.querySelector("#analyticsHistory tbody");

        tbody.innerHTML = "";

        data.logs.forEach(log=>{

            tbody.innerHTML += `

                <tr>

                    <td>${log.id}</td>

                    <td>${log.object_name}</td>

                    <td>${(log.confidence*100).toFixed(1)}%</td>

                    <td>${log.timestamp}</td>

                </tr>

            `;

        });

    }

    catch(error){

        console.error("Analytics Error:", error);

    }

}

// ======================================
// START
// ======================================

refreshAnalytics();

setInterval(refreshAnalytics,1000);