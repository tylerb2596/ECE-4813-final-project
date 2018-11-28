import { Component } from '@angular/core';
import { ContentCollectorService } from "../content/content-collector/content-collector.service";
import { OnInit } from '@angular/core';
import { MatTable } from '@angular/material';
import { Subject } from 'rxjs';

@Component({
    selector: 'content',
    templateUrl: './content.component.html',
    styleUrls: ['./content.component.scss']
  })

  export class ContentComponent {
    public data: any = [];
    public collector: ContentCollectorService;
    public columnsToDisplay = ['state', 'movie', 'sentiment', 'average', 'count'];
    private _dataSubject = new Subject<any[]>();
    public dataObservable = this._dataSubject.asObservable();

    public ngOnInit() {
      this.collector = new ContentCollectorService();
      window.setInterval(() => {
        this.collector.scanData();
        this.data = this.collector.getUsableData();
        this.data.sort((a,b) => {
          return a.state.localeCompare(b.state);
        });
        this._dataSubject.next(this.data);
      }, 3000);
    }

  }