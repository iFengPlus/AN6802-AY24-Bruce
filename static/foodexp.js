function predict_foodexp(){
    const salary = document.getElementById('salary').value;
    console.log("salary: " + salary);
    document.getElementById('foodexp').innerText = "Predicted Food Exp: " + ((salary*0.4851)+147.4)

}