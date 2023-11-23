
const btnsEliminacion = document.querySelectorAll("btnEliminacion");

(function (){
    console.log("text")
    btnsEliminacion.forEach((btn) => {
        btn.addEventListener("click", function (e) {
           e.preventDefault();
            Swal.fire({
                title: "¿Confirma eliminar la máquina?",
                showCancelButton: true,
                confirmButtonText: "Eliminar",
                confirmButtonColor: "#d33",
                backdrop:true,
                showLoaderOnConfirm:true,
                preConfirm:()=>{
                    location.href = e.target.href;
                },
                allowOutsideClick:()=>false,
                allowEscapeKey:()=>false,
            })
        });
    });

})

