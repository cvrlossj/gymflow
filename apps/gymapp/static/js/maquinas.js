document.addEventListener("DOMContentLoaded", async () => {



let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4, 5, 6] },
        { orderable: false, targets: [5, 6] },
        { searchable: false, targets: [0, 5, 6] }
    ],
    pageLength: 10,
    destroy: true
};


const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    await listMaquinas();

    dataTable = $("#datatable_maquinas").DataTable(dataTableOptions);

    dataTableIsInitialized = true;
};

const listMaquinas=async()=>{
    try {   
        const response=await fetch('http://127.0.0.1:8000/list_maquinas/');
        const data=await response.json();

        let content=``;
        data.maquinas.forEach((maquinas,index)=>{
            content+=`
                <tr>
                    <td>${maquinas.id}</td>
                    <td>${maquinas.nombre}</td>
                    <td>${maquinas.zona_muscular}</td>
                    <td>${maquinas.descripcion}</td>
                    <td>${maquinas.imagen}</td>
                    <td>${maquinas.qr_code}</td>
                    <td>
                    <div class="dropdown">
                    <button class="btn btn-secondary btn-sm dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
                        Acción
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton">
                        <li>
                            <a href="${maquinas.qr_code}" download="codigo_qr.png" class="dropdown-item" title="Descargar el código QR">
                                <i class="bi bi-download"></i> Descargar QR
                            </a>
                        </li>
                        <li>
                            <a href="/editarMaquina/${maquinas.id}" class="dropdown-item" title="Editar máquina">
                                <i class="bi bi-pencil-square"></i> Editar
                            </a>
                        </li>
                        <li>
                            <a href="/eliminarMaquina/${maquinas.id}" class="dropdown-item btnEliminacion" title="Eliminar máquina">
                                <i class="bi bi-trash"></i> Eliminar
                            </a>
                        </li>
                    </ul>
                </div>
                    </td>
                </tr>
            `;
        });
    
        tableBody_maquinas.innerHTML= content;
    } catch (ex) {
        alert(ex);
    }
};


window.addEventListener('load', async()=>{
    await initDataTable();
});
});