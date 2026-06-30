import {ChangeDetectorRef, Component, OnInit} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';
import {HttpClient} from '@angular/common/http';
import {AgGridModule} from 'ag-grid-angular';
import {
    ColDef, GridApi, GridReadyEvent, IDatasource, IGetRowsParams,
    ModuleRegistry, InfiniteRowModelModule, ClientSideRowModelModule
} from 'ag-grid-community';
import {ChargeService} from "./charge.service";
import {forkJoin} from "rxjs";

ModuleRegistry.registerModules([InfiniteRowModelModule, ClientSideRowModelModule]);

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [CommonModule, FormsModule, AgGridModule],
    templateUrl: './app.component.html'
})

export class AppComponent implements OnInit {

    totalRows = 0;
    filterName = '';
    filterChargeType = '';
    showModal = false;
    chargeTypes: string[] = [];

    visitTypes: string[] = [];

    newRow = {medical_centre_name: '', patient_visit_type: '', charge_type: '', amount: 0};

    columnDefs: ColDef[] = [];

    defaultColDef: ColDef = {
        sortable: false,
        resizable: true,
        suppressMovable: false,
    };


    private gridApi!: GridApi;

    constructor(
        private http: HttpClient,
        private chargeService: ChargeService,
        private cdr: ChangeDetectorRef
    ) {
    }

    ngOnInit() {
        forkJoin({
            charges: this.chargeService.fetchFilterChargesType(),
            visits: this.chargeService.fetchVisitTypes()
        }).subscribe({
            next: ({charges, visits}) => {
                this.chargeTypes = charges;
                this.visitTypes = visits;
                this.updateColumnDefinition();
            }
        });
    }

    updateColumnDefinition() {
        this.columnDefs = [
            {
                field: 'id', headerName: 'ID', width: 80, editable: false},
            {
                field: 'medical_centre_name', headerName: 'Medical Centre', flex: 2, editable: true},
            {
                field: 'patient_visit_type', headerName: 'Visit Type', flex: 1.5, editable: true},
            {
                field: 'charge_type', headerName: 'Charge Type', flex: 1, editable: true,
                cellEditor: 'agSelectCellEditor',
                cellEditorParams: {values: this.chargeTypes}
            },
            {
                field: 'amount', headerName: 'Amount (Rs.)', flex: 1, editable: true,
                valueFormatter: p => p.value != null ? `Rs.${Number(p.value).toFixed(2)}` : ''
            }
        ];
    }

    onGridReady(event: GridReadyEvent) {
        this.gridApi = event.api;
        this.setDatasource();

        this.gridApi.addEventListener('cellValueChanged', (e: any) => {
            const {data, colDef, newValue} = e;
            if (!data?.id) return;
            const payload: any = {};
            payload[colDef.field] = colDef.field === 'amount' ? Number(newValue) : newValue;

            this.chargeService.updateCharge(data.id, payload)
                .subscribe({
                    error: err => console.error('Update failed', err)
                });
        });
    }

    setDatasource() {
        const datasource: IDatasource = {
            getRows: (params: IGetRowsParams) => {
                this.chargeService.getCharges(params.startRow, params.endRow, this.filterChargeType, this.filterName)
                    .subscribe({
                        next: res => {
                            this.totalRows = res.total;
                            this.cdr.detectChanges();
                            params.successCallback(res.rows, res.total);
                        },
                        error: () => params.failCallback()
                    });
            }
        };
        this.gridApi.setDatasource(datasource);
    }

    onFilterChange() {
        if (this.gridApi) {
            this.setDatasource();
        }
    }

    resetFilters() {
        this.filterName = '';
        this.filterChargeType = '';
        this.onFilterChange();
    }

    refreshGrid() {
        this.setDatasource();
    }

    openAddModal() {
        this.newRow = {medical_centre_name: '', patient_visit_type: '', charge_type: '', amount: 0};
        this.showModal = true;
    }

    closeModal() {
        this.showModal = false;
    }

    submitNewRow() {
        if (!this.newRow.medical_centre_name || !this.newRow.patient_visit_type || !this.newRow.charge_type) {
            alert('Please fill in all fields.');
            return;
        }

        this.chargeService.createCharge(this.newRow)
            .subscribe({
                next: () => {
                    this.closeModal();
                    this.refreshGrid();
                },
                error: err => {
                    console.error('Create failed', err);
                    alert('Failed to create record.');
                }
            });
    }
}
