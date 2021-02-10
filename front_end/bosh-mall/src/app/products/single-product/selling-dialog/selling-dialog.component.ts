import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-selling-dialog',
  templateUrl: './selling-dialog.component.html',
  styleUrls: ['./selling-dialog.component.sass']
})
export class SellingDialogComponent implements OnInit {

  constructor(public dialog: MatDialog) { }

  closeD(): void {
    this.dialog.closeAll();
  }

  ngOnInit(): void {
  }

}
