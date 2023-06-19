function loadValues(){
    let selectedName = document.getElementById("name-dropdown").value;

    fetch(/get_data/ + selectedName)
        .then(response => response.json())
        .then(data =>{
            document.getElementById("perc").textContent = data.perc;
            document.getElementById("stdv").textContent = data.stdv;
            document.getElementById("avg").textContent = data.avg;

            document.getElementById("sub-data").style.display = "";
            //displays new form
        });
}

