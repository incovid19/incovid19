
var feedPath = '';
var isDeactive = 0;
if(!window.jQuery)
{
   var script = document.createElement('script');
   script.type = "text/javascript";
   script.src = "/sites/all/themes/mygov/js/jquery.3.4.1.js";
   document.getElementsByTagName('head')[0].appendChild(script);
}

function querySt(e) {hu = window.location.search.substring(1).split("&");for (i = 0; i < hu.length; i++) {ft = hu[i].split("=");if (ft[0] == e) {return ft[1];}}}

var hidetable = '';
var device = '';
var dm = querySt("dm") || '';
var custfeed = querySt("custfeed") || '';
var custfeedTime = querySt("custfeedTime") || '';
var desktop = querySt("desktop") || '';
var hideads = querySt("hideads") || 0;

var tableheight = 'auto';

var appsCss = '';
var chbckcolor = '#ffffff';

var styleCss = `<style>table {border-collapse: collapse;border-spacing: 0;word-break: normal;}
        .ind-mp_wrap {
            width: 100%;
            background-color: #fff;
        }
        
        .ind-mp_data {
            width: 100%; margin-bottom:40px;
        }

        .ind-mp_total {
            width: 100%;
        }

        .ind-mp_total_list {
            width: 100%;
            display: flex;
            justify-content: space-between;
            padding: 0px 10px 5px 10px;
        }

        .ind-mp_total_iteam {
            width: 20%;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            font-size: 13px;
            line-height: 1.4;
        }

        .ind-mp_total_iteam span {
            display: block;
            width: 100%;
            text-align: center;
        }

        .ind-mp_num {
            font-size: 24px;
            font-weight: 600;
        }

        .ind-mp_txt {
            font-size: 12px;
            color: #888888;
            font-weight: 500;
            text-transform: uppercase;
        }

        .confirmed,
        .confirmed a {
            color: #4C4C4C;
        }

        .confirmed .ind-mp_txt {
            color: rgba(162, 162, 162, 1);
        }

        .activecase,
        .activecase a {
            color: #3A81D8;
        }

        .activecase .ind-mp_txt {
            color: rgba(129, 166, 211, 1)
        }

        .recovered,
        .recovered a {
            color: #4F9A0B;
        }

        .recovered .ind-mp_txt {
            color: rgba(128, 183, 79, 1)
        }

        .deaths,
        .deaths a {
            color: #CC362C;
        }

        .deaths .ind-mp_txt {
            color: rgba(201, 112, 107, 1)
        }

        .ind-mp_info {
            display: flex;
            flex-wrap: nowrap;
            white-space: nowrap;
            position: relative;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            /*overflow-y: hidden;*/
            padding-bottom: 5px;
            
        }

        .ind-center_api_tbl {
            width: 100%; margin-top:0px;
        }

        .ind-center_api_tbl thead {
            width: 100%;
        }

        .ind-center_api_tbl th:nth-of-type(1) {
            background-color: rgba(234, 234, 234, .38);
            color: #4C4C4C;
            border-right: solid 1px #fff;
        }

        .ind-center_api_tbl th:nth-of-type(2) {
            background: #d3a70f; /* Old browsers */
background: -moz-linear-gradient(top,  #d3a70f 0%, #f6d04a 100%); /* FF3.6-15 */
background: -webkit-linear-gradient(top,  #d3a70f 0%,#f6d04a 100%); /* Chrome10-25,Safari5.1-6 */
background: linear-gradient(to bottom,  #d3a70f 0%,#f6d04a 100%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#d3a70f', endColorstr='#f6d04a',GradientType=0 ); /* IE6-9 */
            color: #582801;
            border-right: solid 1px #fff;
        }

        .ind-center_api_tbl th:nth-of-type(3),.ind-center_api_tbl th:nth-of-type(6) {
            background: #a5c9fd; /* Old browsers */
background: -moz-linear-gradient(top,  #a5c9fd 0%, #bde5fc 100%); /* FF3.6-15 */
background: -webkit-linear-gradient(top,  #a5c9fd 0%,#bde5fc 100%); /* Chrome10-25,Safari5.1-6 */
background: linear-gradient(to bottom,  #a5c9fd 0%,#bde5fc 100%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#a5c9fd', endColorstr='#bde5fc',GradientType=0 ); /* IE6-9 */

            color: #002c57;
            border-right: solid 1px #fff;
        }

        .ind-center_api_tbl th:nth-of-type(4),.ind-center_api_tbl th:nth-of-type(7) {
           background: #9be89c; /* Old browsers */
background: -moz-linear-gradient(top,  #9be89c 0%, #cdf97d 100%); /* FF3.6-15 */
background: -webkit-linear-gradient(top,  #9be89c 0%,#cdf97d 100%); /* Chrome10-25,Safari5.1-6 */
background: linear-gradient(to bottom,  #9be89c 0%,#cdf97d 100%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#9be89c', endColorstr='#cdf97d',GradientType=0 ); /* IE6-9 */
            color: #005c25;
            border-right: solid 1px #fff;
        }

        .ind-center_api_tbl th:nth-of-type(5),.ind-center_api_tbl th:nth-of-type(8) {
            background: #fe8683; /* Old browsers */
background: -moz-linear-gradient(top,  #fe8683 0%, #ff9d9b 100%); /* FF3.6-15 */
background: -webkit-linear-gradient(top,  #fe8683 0%,#ff9d9b 100%); /* Chrome10-25,Safari5.1-6 */
background: linear-gradient(to bottom,  #fe8683 0%,#ff9d9b 100%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#fe8683', endColorstr='#ff9d9b',GradientType=0 ); /* IE6-9 */
            color: #5a0401;
        }
        .ind-center_api_tbl th:nth-of-type(5){border-right: solid 1px #fff;}

        .ind-center_api_tbl td:nth-of-type(1) {
            color: #6A6A6A;
        }

        .ind-center_api_tbl td:nth-of-type(2) {
            color: #582801;
        }

        .ind-center_api_tbl td:nth-of-type(3),.ind-center_api_tbl td:nth-of-type(6) {
            color: #002c57;
        }

        .ind-center_api_tbl td:nth-of-type(4),.ind-center_api_tbl td:nth-of-type(7) {
            color: #005c25;
        }

        .ind-center_api_tbl td:nth-of-type(5),.ind-center_api_tbl td:nth-of-type(8) {
            color: #5a0401;
        }
        .ind-center_api_tbl td:nth-of-type(4) .data-up{background: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAOCAYAAAAWo42rAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyBpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEzNDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNSBXaW5kb3dzIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOkQ2REMwOUJGREUyQTExRUFBNkVBRDlDMjI1NzEyNUVBIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOkQ2REMwOUMwREUyQTExRUFBNkVBRDlDMjI1NzEyNUVBIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6RDZEQzA5QkRERTJBMTFFQUE2RUFEOUMyMjU3MTI1RUEiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6RDZEQzA5QkVERTJBMTFFQUE2RUFEOUMyMjU3MTI1RUEiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz7NOUITAAAA7klEQVR42mL4//8/AwzzzkxwBOJ8ZDEYZgQRIMA3K5EdSC0DYicgtvyUNv8GAxJgQmLHAbEfEAsAcTdQIxeGQqCgNpBqBGIWqLgPEKcgK2QEuokDSK8BYm8GVPAMiH2BTjgHMzEfiyIQkII6QRCmMBqIvwPxLyRFv4H4AxBbA7EnTKEDEIsBcRmSwodAbAsV3wR2I1LwgHTvAWKQm78CcQDQfXuwBQ/I0QegbG4gDsYajkDdIHe2A/EbqFA80BY3bCaCFB8CUklAfA+IOYF4ElCxLoobkQFQUgNIpULxKyAuwaoQSYMrkAoFGQgQYACL/VkWKlnALQAAAABJRU5ErkJggg==') left center no-repeat; color: #4F9A0B; background-size: auto 11px;}


        .ind-center_api_tbl tr {
            width: 100%;
            white-space: nowrap;
        }

        .ind-center_api_tbl th:nth-of-type(1),
        .ind-center_api_tbl td:nth-of-type(1) {
            width: 30%;
            text-align: left;
            white-space: normal; 
        }

        .ind-center_api_tbl th:nth-of-type(2),
        .ind-center_api_tbl td:nth-of-type(2) {
            width: 15%;
        }

        .ind-center_api_tbl th:nth-of-type(3),
        .ind-center_api_tbl td:nth-of-type(3) {
            width: 15%;
        }

        .ind-center_api_tbl th:nth-of-type(4),
        .ind-center_api_tbl td:nth-of-type(4) {
            width: 15%;
        }

        .ind-center_api_tbl th:nth-of-type(5),
        .ind-center_api_tbl td:nth-of-type(5) {
            width: 15%;
            min-width: 85px; 
        }


        .ind-center_api_tbl tbody {
            width: 100%;
        }

        .ind-center_api_tbl tbody tr {
           cursor: pointer;
           background:none;
        }
        
        .ind-center_api_tbl td, .ind-center_api_tbl th {
          border: 1px solid #ddd;
          cursor:default;
        }
        .ind_center_api_tbl tr th{cursor:pointer;}
        .ind-center_api_tbl tr:nth-child(even){background-color: #f2f2f2;}
        
        .ind-center_api_tbl tbody tr:hover {background-color: #ddd;}
        .ind-center_api_tbl th,
        .ind-center_api_tbl td {
            padding: 10px;
            font-size: 14px;
            color: #706A6C;
            font-weight: 500;
            text-align: center;
            position: relative;
            text-transform: uppercase;
            min-width: 110px;
            letter-spacing: -0.5px;
        }

        .ind-center_api_tbl th {
            font-weight: 900; cursor:pointer
        }

        .ind-center_api_tbl td{ font-size: 14px;text-transform: capitalize;}
        

        .sortable th::after {
            content: "";
            display: inline-block;
            position: relative;
            top: 0px;
            left: 5px;
            width: 10px;
            height: 10px;
            background: url(data:image/svg+xml;utf8;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iaXNvLTg4NTktMSI/Pgo8IS0tIEdlbmVyYXRvcjogQWRvYmUgSWxsdXN0cmF0b3IgMTYuMC4wLCBTVkcgRXhwb3J0IFBsdWctSW4gLiBTVkcgVmVyc2lvbjogNi4wMCBCdWlsZCAwKSAgLS0+CjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+CjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgdmVyc2lvbj0iMS4xIiBpZD0iQ2FwYV8xIiB4PSIwcHgiIHk9IjBweCIgd2lkdGg9IjE2cHgiIGhlaWdodD0iMTZweCIgdmlld0JveD0iMCAwIDQwMS45OTggNDAxLjk5OCIgc3R5bGU9ImVuYWJsZS1iYWNrZ3JvdW5kOm5ldyAwIDAgNDAxLjk5OCA0MDEuOTk4OyIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSI+CjxnPgoJPGc+CgkJPHBhdGggZD0iTTczLjA5MiwxNjQuNDUyaDI1NS44MTNjNC45NDksMCw5LjIzMy0xLjgwNywxMi44NDgtNS40MjRjMy42MTMtMy42MTYsNS40MjctNy44OTgsNS40MjctMTIuODQ3ICAgIGMwLTQuOTQ5LTEuODEzLTkuMjI5LTUuNDI3LTEyLjg1TDIxMy44NDYsNS40MjRDMjEwLjIzMiwxLjgxMiwyMDUuOTUxLDAsMjAwLjk5OSwwcy05LjIzMywxLjgxMi0xMi44NSw1LjQyNEw2MC4yNDIsMTMzLjMzMSAgICBjLTMuNjE3LDMuNjE3LTUuNDI0LDcuOTAxLTUuNDI0LDEyLjg1YzAsNC45NDgsMS44MDcsOS4yMzEsNS40MjQsMTIuODQ3QzYzLjg2MywxNjIuNjQ1LDY4LjE0NCwxNjQuNDUyLDczLjA5MiwxNjQuNDUyeiIgZmlsbD0iIzAwMDAwMCIvPgoJCTxwYXRoIGQ9Ik0zMjguOTA1LDIzNy41NDlINzMuMDkyYy00Ljk1MiwwLTkuMjMzLDEuODA4LTEyLjg1LDUuNDIxYy0zLjYxNywzLjYxNy01LjQyNCw3Ljg5OC01LjQyNCwxMi44NDcgICAgYzAsNC45NDksMS44MDcsOS4yMzMsNS40MjQsMTIuODQ4TDE4OC4xNDksMzk2LjU3YzMuNjIxLDMuNjE3LDcuOTAyLDUuNDI4LDEyLjg1LDUuNDI4czkuMjMzLTEuODExLDEyLjg0Ny01LjQyOGwxMjcuOTA3LTEyNy45MDYgICAgYzMuNjEzLTMuNjE0LDUuNDI3LTcuODk4LDUuNDI3LTEyLjg0OGMwLTQuOTQ4LTEuODEzLTkuMjI5LTUuNDI3LTEyLjg0N0MzMzguMTM5LDIzOS4zNTMsMzMzLjg1NCwyMzcuNTQ5LDMyOC45MDUsMjM3LjU0OXoiIGZpbGw9IiMwMDAwMDAiLz4KCTwvZz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8L3N2Zz4K) center center no-repeat;
            background-size: 100%;
            opacity: 0.5;
        }

        .sortable th.sorttable_sorted::after {
            content: "";
            display: inline-block;
            position: relative;
            top: 0px;
            left: 5px;
            width: 9px;
            height: 8px;
            background: url(data:image/svg+xml;utf8;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iaXNvLTg4NTktMSI/Pgo8IS0tIEdlbmVyYXRvcjogQWRvYmUgSWxsdXN0cmF0b3IgMTYuMC4wLCBTVkcgRXhwb3J0IFBsdWctSW4gLiBTVkcgVmVyc2lvbjogNi4wMCBCdWlsZCAwKSAgLS0+CjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+CjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgdmVyc2lvbj0iMS4xIiBpZD0iQ2FwYV8xIiB4PSIwcHgiIHk9IjBweCIgd2lkdGg9IjUxMnB4IiBoZWlnaHQ9IjUxMnB4IiB2aWV3Qm94PSIwIDAgMjkyLjM2MiAyOTIuMzYyIiBzdHlsZT0iZW5hYmxlLWJhY2tncm91bmQ6bmV3IDAgMCAyOTIuMzYyIDI5Mi4zNjI7IiB4bWw6c3BhY2U9InByZXNlcnZlIj4KPGc+Cgk8cGF0aCBkPSJNMjg2LjkzNSwxOTcuMjg2TDE1OS4wMjgsNjkuMzc5Yy0zLjYxMy0zLjYxNy03Ljg5NS01LjQyNC0xMi44NDctNS40MjRzLTkuMjMzLDEuODA3LTEyLjg1LDUuNDI0TDUuNDI0LDE5Ny4yODYgICBDMS44MDcsMjAwLjksMCwyMDUuMTg0LDAsMjEwLjEzMnMxLjgwNyw5LjIzMyw1LjQyNCwxMi44NDdjMy42MjEsMy42MTcsNy45MDIsNS40MjgsMTIuODUsNS40MjhoMjU1LjgxMyAgIGM0Ljk0OSwwLDkuMjMzLTEuODExLDEyLjg0OC01LjQyOGMzLjYxMy0zLjYxMyw1LjQyNy03Ljg5OCw1LjQyNy0xMi44NDdTMjkwLjU0OCwyMDAuOSwyODYuOTM1LDE5Ny4yODZ6IiBmaWxsPSIjMDAwMDAwIi8+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPC9zdmc+Cg==) center center no-repeat;
            background-size: 100%;
            opacity: 0.5;
            transform: rotate(180deg);
        }


        .sortable th.sorttable_sorted_reverse::after {
            content: "";
            display: inline-block;
            position: relative;
            top: 0px;
            left: 5px;
            width: 9px;
            height: 10px;
            background: url(data:image/svg+xml;utf8;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iaXNvLTg4NTktMSI/Pgo8IS0tIEdlbmVyYXRvcjogQWRvYmUgSWxsdXN0cmF0b3IgMTYuMC4wLCBTVkcgRXhwb3J0IFBsdWctSW4gLiBTVkcgVmVyc2lvbjogNi4wMCBCdWlsZCAwKSAgLS0+CjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+CjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgdmVyc2lvbj0iMS4xIiBpZD0iQ2FwYV8xIiB4PSIwcHgiIHk9IjBweCIgd2lkdGg9IjUxMnB4IiBoZWlnaHQ9IjUxMnB4IiB2aWV3Qm94PSIwIDAgMjkyLjM2MiAyOTIuMzYyIiBzdHlsZT0iZW5hYmxlLWJhY2tncm91bmQ6bmV3IDAgMCAyOTIuMzYyIDI5Mi4zNjI7IiB4bWw6c3BhY2U9InByZXNlcnZlIj4KPGc+Cgk8cGF0aCBkPSJNMjg2LjkzNSwxOTcuMjg2TDE1OS4wMjgsNjkuMzc5Yy0zLjYxMy0zLjYxNy03Ljg5NS01LjQyNC0xMi44NDctNS40MjRzLTkuMjMzLDEuODA3LTEyLjg1LDUuNDI0TDUuNDI0LDE5Ny4yODYgICBDMS44MDcsMjAwLjksMCwyMDUuMTg0LDAsMjEwLjEzMnMxLjgwNyw5LjIzMyw1LjQyNCwxMi44NDdjMy42MjEsMy42MTcsNy45MDIsNS40MjgsMTIuODUsNS40MjhoMjU1LjgxMyAgIGM0Ljk0OSwwLDkuMjMzLTEuODExLDEyLjg0OC01LjQyOGMzLjYxMy0zLjYxMyw1LjQyNy03Ljg5OCw1LjQyNy0xMi44NDdTMjkwLjU0OCwyMDAuOSwyODYuOTM1LDE5Ny4yODZ6IiBmaWxsPSIjMDAwMDAwIi8+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPGc+CjwvZz4KPC9zdmc+Cg==) center center no-repeat;
            background-size: 100%;
            opacity: 0.5;
            
        }

        .minigraph {
            width: 100%;
            padding: 0px 10px 5px 10px;
            align-self: center;
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            margin: 0;
        }
        .minigraph li {height: 75px;width:20%;}
        .svg-parent {
            flex-shrink: 0;
            width: 20%;
            display: flex;
            align-items: flex-end;
        }

        .svg-parent svg {
            width: 100%;
        }
        .data-down-up {
            color: #4F9A0B;
            font-weight: 400;
            background: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAOCAYAAAAWo42rAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyBpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEzNDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNSBXaW5kb3dzIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOkQ2REMwOUJGREUyQTExRUFBNkVBRDlDMjI1NzEyNUVBIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOkQ2REMwOUMwREUyQTExRUFBNkVBRDlDMjI1NzEyNUVBIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6RDZEQzA5QkRERTJBMTFFQUE2RUFEOUMyMjU3MTI1RUEiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6RDZEQzA5QkVERTJBMTFFQUE2RUFEOUMyMjU3MTI1RUEiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz7NOUITAAAA7klEQVR42mL4//8/AwzzzkxwBOJ8ZDEYZgQRIMA3K5EdSC0DYicgtvyUNv8GAxJgQmLHAbEfEAsAcTdQIxeGQqCgNpBqBGIWqLgPEKcgK2QEuokDSK8BYm8GVPAMiH2BTjgHMzEfiyIQkII6QRCmMBqIvwPxLyRFv4H4AxBbA7EnTKEDEIsBcRmSwodAbAsV3wR2I1LwgHTvAWKQm78CcQDQfXuwBQ/I0QegbG4gDsYajkDdIHe2A/EbqFA80BY3bCaCFB8CUklAfA+IOYF4ElCxLoobkQFQUgNIpULxKyAuwaoQSYMrkAoFGQgQYACL/VkWKlnALQAAAABJRU5ErkJggg==') left center no-repeat;
            position: absolute;
            padding-left: 12px;
            font-size: 12px;
            margin-left: 5px;
            top: 50%;
            transform: translateY(-50%);
            background-size: auto 11px;
        }

        .data-up {
            color: #C9706B;
            font-weight: 400;
            background: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAOCAYAAAAWo42rAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyBpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEzNDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNSBXaW5kb3dzIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOkM4NEQzNjJDREUyQjExRUE5NUU1QUQyMjE4NzEyNTVGIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOkM4NEQzNjJEREUyQjExRUE5NUU1QUQyMjE4NzEyNTVGIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6Qzg0RDM2MkFERTJCMTFFQTk1RTVBRDIyMTg3MTI1NUYiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6Qzg0RDM2MkJERTJCMTFFQTk1RTVBRDIyMTg3MTI1NUYiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz6a996BAAAA9ElEQVR42mL4//8/Awy/VpN3BOJ8ZDEYZgQRIPBGXYEdSC0DYicgthS5+eAGAxJgQmLHAbEfEAsAcTdQIxeGQqCgNpBqBGIWqLgPEKcgK2QEuokDSK8BYm8GVPAMiH2BTjgHMzEfiyIQkII6QRCmMBqIvwPxLyRFv4H4AxBbA7EnTKEDEIsBcRmSwodAbAsV3wQSYAG64R3UQ2eA1A8gBrlZEoglgHJXsAUPyNEHoGxuIA7GGo5A3SB3toMMhwrFA21xw2YiSPEhIJUExPeAmBOIJwEV64LDERaFyAAoqQGkUqH4FRCXYFWIpMEVSIWCDAQIMADJA1nORkVBawAAAABJRU5ErkJggg==') left center no-repeat;
            position: absolute;
            padding-left: 12px;
            font-size: 12px;
            margin-left: 5px;
            top: 50%;
            transform: translateY(-50%);
            background-size: auto 11px;
        }

        .data-down {
            color: #4F9A0B;
            font-weight: 400;
            background: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAOCAYAAAAWo42rAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyBpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEzNDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNSBXaW5kb3dzIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjkwMUVEMDVFREUyQjExRUE5OTM1QkVCMzhCRjI5MjBDIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjkwMUVEMDVGREUyQjExRUE5OTM1QkVCMzhCRjI5MjBDIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6OTAxRUQwNUNERTJCMTFFQTk5MzVCRUIzOEJGMjkyMEMiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6OTAxRUQwNURERTJCMTFFQTk5MzVCRUIzOEJGMjkyMEMiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz7Q/SPjAAAA9klEQVR42mLknZkwm4GB4T8Qr/6UNn83Aw7ABMRbgdgJiNfyzUrsBWINbAoZ////zwCU1AWZCMTqQHwPiAuApm/GUAgCQMVuQGoDEHMC8RsgDgYqPoRsNRgABXcBqYVQrggQVwI1c2IohIK1QPwVynYAYiN0N/JANckB8XogVoHKFwDxXCBmg5noB8SvgPgwEMsj2dAFFT8AU7gdiI8CsQAQsyIpZIN6bimyr0HuAQWJFJq7QeEcguzrc0CqE03RcyAuB8r9QPf1HCDeAmX/AeJ6oKKrGMEDFPwGpEqB+AMQbwLiRXBJkBvRMTCh5AOxI7IYQIABAAbgY7KwlwlIAAAAAElFTkSuQmCC') left center no-repeat;
            position: absolute;
            padding-left: 12px;
            font-size: 12px;
            margin-left: 5px;
            top: 50%;
            transform: translateY(-50%);
            background-size: auto 11px;
        }
        .map_dcm-wrp {
            margin-top: 5px;
            position: relative;
        }
        .map_dcm-wrp.btm-legend {
            padding: 10px;
            margin-top: 0;
        }
        .map_dcm-wrp.btm-legend .map_dcm-txt {
            margin-top: 5px;
        }
        .btm-legend .map_dcm-txt span {
            position: relative;
            left: 0;
            top: 0;
        }
        .map_dcm-ttl {
            color: #555;
            font-size: 12px;
            margin-bottom: 2px;
        }

        .map_dcm-txt,
        .map_dcm-txt a {
            color: #555;
            font-size: 12px;
            line-height: 16px;
        }
        p.mid-wrap {
            text-align: right;
            position: relative;
            transform: translateX(-50%);
            display: inline-block;
            margin: 0;
            line-height: normal;
        }
        p.mid-wrap1{margin: 0; line-height: normal;}
        .ind-mp_total_iteam span.ind-mp_num {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding-bottom: 15px;
        }

        .ind-mp_total_iteam span.ind-mp_num .data-up, .ind-mp_total_iteam span.ind-mp_num .data-down, .ind-mp_total_iteam span.ind-mp_num .data-down-up {position: absolute;left: 50%;top: auto;bottom: 2px;transform: translate(-50%, 0);width: auto;margin: 0px;font-weight: bold;}
        @media only screen and (max-width: 500px) {
            body {font-family: -apple-system, 'Arial', 'Helvetica';}
            .ind-center_api_tbl th, .ind-center_api_tbl td { min-width: 120px; }
            .ind-center_api_tbl {
                height: `+tableheight+`;
                position: relative;
                overflow-y: hidden;
                display: block;
            }
            .ind-mp_total_iteam{width: auto;}
            .ind-mp_num {font-size: 17px;}
            .ind-mp_info .ind-mp_more {
                width: 100%;
                height: 100px;
                position: absolute;
                text-align: center;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgb(255, 255, 255);
                background: linear-gradient(0deg, rgba(255, 255, 255, 1) 0%, rgba(255, 255, 255, 0) 100%);
            }
            .ind-mp_more-btn {
                background-color: #ffffff;
                border: 1px solid #f1f1f1;
                border-radius: 50px;
                box-shadow: 0 0px 10px rgba(0, 0, 0, 0.1);
                color: #3a81d8;
                display: inline-block;
                font-size: 12px;
                font-weight: 500;
                line-height: 1.6;
                margin: 0 auto;
                padding: 3px 15px;
                position: absolute;
                left: 50%;
                transform: translateX(-50%);
                bottom: 10px;
                text-decoration: none;
                text-transform: capitalize;
            }
            .full-data-show.ind-mp_info .ind-mp_more {
                display: none;
            }
            .full-data-show .ind-center_api_tbl {
                height: auto;
            }
}
`+appsCss+`
</style>`;

if(hidetable == 1) {
}
function showCenterAPITableData(){
    var addHtml = `<div class="ind-mp_data">
            <div class="ind-mp_info">
                <table class="ind-center_api_tbl sortable" id="ind_center_api_tbl">
                    <thead>
                        <tr>
                            <th>Center Name</th>
                            <th>Location</th>
                            <th>Vaccine Name</th>  
                            <th>Age</th>
                            <th>Available Dose</th> 
                            <th>Fee Type</th>
                             <th>Available Date</th>
                        </tr>
                    </thead><tbody></tbody>
                </table>
                `+(device=='mobile'?'<div class="ind-mp_more"><a href="javascript:void(0);" class="ind-mp_more-btn">Show More</a></div>':'')+`
            </div>`; 
    if(jQuery( "#lang .actv" ).html() != "English"){
        addHtml = `<div class="ind-mp_data">
            <div class="ind-mp_info">
                <table class="ind-center_api_tbl sortable" id="ind_center_api_tbl">
                    <thead>
                        <tr>
                            <th>केंद्र का नाम</th>
                            <th>स्थान</th>
                            <th>वैक्सीन का नाम</th>  
                            <th>उम्र</th>
                            <th>उपलब्ध डोज</th> 
                            <th>शुल्क के प्रकार</th> 
                             <th>उपलब्ध तारीख</th>
                        </tr>
                    </thead><tbody></tbody>
                </table>
                `+(device=='mobile'?'<div class="ind-mp_more"><a href="javascript:void(0);" class="ind-mp_more-btn">Show More</a></div>':'')+`
            </div>`;
    }
jQuery('#_centers_list_api').html(styleCss+addHtml);
 var ts = Math.round((new Date()).getTime() / 1000);
    var prev = ts - (ts % 1800);
    next = prev - 0;
   /* var gatData =  '/sites/default/files/covid/vaccine/vaccination_states.json';
    var tableData = '<option value="">Select State</option>';
   
    jQuery.ajax({
        type: 'GET',
        url: gatData + '?timestamp=' + next,
        dataType: 'json',
        timeout: 6000,
        async: false,  //set false if load map with data
        success: function(response) { 
            var a = response
            for(var k = 0; k < a.length; k++){
                 tableData += '<option value="'+a[k]['state_id']+'">'+a[k]['state_name']+'</option>';

                if(tableData != '' && hidetable != 1){
                    jQuery('#api_state').html(tableData);
                }
            }  
        },
        error: function() {

        },
        complete: function() {

        }
    });*/
    
    jQuery(".date_section .filter-bydate a").click( function() {
        if(!jQuery(this).hasClass("date-active")){
            jQuery(".date_section .filter-bydate a").removeClass("date-active");
            jQuery(this).addClass("date-active");
             var isDeactive = 0;
        }else{  
            jQuery(this).removeClass("date-active");
             var isDeactive = 1;
        }
        
    });
   
}

function stateDistrict(){
    var api_state = jQuery("#api_state").val();
    var gatData =  '/sites/default/files/covid/vaccine/vaccination_districts.json';
    if(jQuery( "#lang .actv" ).html() == "English"){
        var tableData = '<option value="">Select District</option>';   
    }else{
        var tableData = '<option value="">जिला चुनें</option>'; 
    } 
    var ts = Math.round((new Date()).getTime() / 1000);
    var prev = ts - (ts % 1800);
    next = prev - 0;
    jQuery.ajax({
        type: 'GET',
        url: gatData + '?timestamp=' + next,
        dataType: 'json',
        timeout: 6000,
        async: false,  //set false if load map with data
        success: function(response) { 
           var  a = response;
            for(var k = 0; k < a.length; k++){
                if(api_state == a[k]['state_id']){
                     tableData += '<option value="'+a[k]['district_id']+'">'+a[k]['district_name']+'</option>';
                 
                }
                if(tableData != '' && hidetable != 1){
                    jQuery('#api_district').html(tableData);
                }
            }  
        },
        error: function() {

        },
        complete: function() {

        }
    });
}


function searchKeyAPICenter(sDate = '') {
    var ts = Math.round((new Date()).getTime() / 1000);
    var prev = ts - (ts % 1800);
    next = prev - 0;
    jQuery("#api_centername").val('');
    jQuery("#api_location").val('');
    jQuery("#api_payment_type").val('');
    jQuery("#api_vaccine_type").val('');
    jQuery("#api_age").val('');
     if(sDate == ''){
        jQuery(".filter-bydate a").removeClass("date-active");
    }
    var str = '';
    var api_pincode = jQuery("#api_pincode").val();
    if(api_pincode != ''){
        str = '&pincode='+api_pincode;            
    }
    var api_state = jQuery("#api_state").val();
    if(api_state != '0' && api_state != '' && api_state != null){
        str = str+'&state_id='+api_state;
    }
    var api_district = jQuery("#api_district").val();
    if(api_district != ''){
        str = str+'&district_id='+api_district;
    }
    if(jQuery("li.dist").hasClass("active")){
         if(api_state == ''){
            alert("Please select State");
            return false;
         }else{
            if(api_district == ''){
                alert("Please select District");
                return false;
            }
        }
    }
    if(jQuery("li.pin").hasClass("active")){
        if(api_pincode == ''){
            alert("Please enter pin code");
            return false;
        }else if(parseInt(api_pincode) < 100000 || parseInt(api_pincode) > 999999 || isNaN(parseInt(api_pincode))){
            alert("Please enter valid pin code");
            return false;
        }
    }

    jQuery(".filter_cat").show();
    jQuery(".date_section").show();
    jQuery('#ind_center_api_tbl tbody').html('');
    jQuery(".date_section img.loader").show();
    //var gatData =  '/cowin-vaccine-center/?page=0&page_size=200'+str;  
       
    var gatData = 'https://api.mygov.in/get-vaccination-center/?api_key=57076294a5e2ab7fe0000001dd278c47e313412c7de416e536f1992f'+str;
           
    var vacName = Array(); 
    vacName[1] = "COVISHIELD";
    vacName[2] = "COVAXIN";
    vacName[3] = "SPUTNIK V";
    jQuery(".filter-bydate a").removeClass("date-active");
    var tableData = '';
    jQuery.ajax({
        type: 'GET',
        url: gatData,
        dataType: 'json',
        timeout: 600000,
        success: function(response) { 

            var a = response['center_data'];
            if(a.length == 0){
                if(jQuery( "#lang .actv" ).html() == "English"){
                    jQuery("#ind_center_api_tbl tbody").html('<tr id="no_row_found"><td valign="top" colspan="8" class="dataTables_empty">No matching records found</td></tr>');
                }else{
                    jQuery("#ind_center_api_tbl tbody").html('<tr id="no_row_found"><td valign="top" colspan="8" class="dataTables_empty">मिलता-जुलता कोई रिकॉर्ड नहीं मिला</td></tr>');
                }
                 
                 jQuery(".date_section .loader").hide();
            }else{
                var cntData = 0;
                for(var k = 0; k < a.length; k++){
                    var j = stateJsonData[k];
                    
                    if(sDate == ''){
                            //if(a[k]['available_capacity_dose1'] >= 0){
                                tableData += '<tr><td>'+a[k]['name']+'</td><td>'+a[k]['location']+'</td><td>'+a[k]['vaccine_name']+'</td><td>'+a[k]['min_age_limit']+'</td><td><div class="d1"><strong>D1</strong><br />'+a[k]['available_capacity_dose1']+'</div><div class="d2"><strong>D2</strong><br />'+a[k]['available_capacity_dose2']+'</div></td><td>'+a[k]['fee_type']+'</td><td>'+a[k]['next_available_day']+'</td></tr>';
                            /*}
                            if(a[k]['available_capacity_dose2'] >= 0){
                                tableData += '<tr><td>'+a[k]['name']+'</td><td>'+a[k]['location']+'</td><td>'+a[k]['vaccine_name']+'</td><td>'+a[k]['min_age_limit']+'</td><td>'+a[k]['available_capacity_dose2']+' - D2</td><td>'+a[k]['fee_type']+'</td><td>'+a[k]['next_available_day']+'</td></tr>';
                            }*/
                                
                    }else{
                        var value = a[k]; 
                        if(value['sessions_list'][sDate] === undefined)
                        {
                            //
                        }else{
                            cntData ++;
                            for(var i = 0; i < value['sessions_list'][sDate].length; i++){
                                var val = value['sessions_list'][sDate][i];
                                var vacID = val['vaccine'];
                               // if(a[k]['available_capacity_dose1'] >= 0){
                                     tableData += '<tr><td>'+a[k]['name']+'</td><td>'+a[k]['location']+'</td><td>'+vacName[vacID]+'</td><td>'+val['min_age_limit']+'</td><td><div class="d1"><strong>D1</strong><br />'+val['available_capacity_dose1']+'</div><div class="d2"><strong>D2</strong><br />'+val['available_capacity_dose2']+'</div></td><td>'+a[k]['fee_type']+'</td><td>'+val['date']+'</td></tr>';
                               /* }
                                if(a[k]['available_capacity_dose2'] >= 0){
                                    tableData += '<tr><td>'+a[k]['name']+'</td><td>'+a[k]['location']+'</td><td>'+a[k]['vaccine_name']+'</td><td>'+val['min_age_limit']+'</td><td>'+val['available_capacity_dose2']+' -D2</td><td>'+a[k]['fee_type']+'</td><td>'+val['date']+'</td></tr>';
                                }*/
                               
                            }
                        }   
                    } 
                    
                    if(cntData == 0 && sDate != ''){
                      if(jQuery( "#lang .actv" ).html() == "English"){
                            jQuery("#ind_center_api_tbl tbody").html('<tr id="no_row_found"><td valign="top" colspan="8" class="dataTables_empty">No matching records found!!</td></tr>');
                        }else{
                            jQuery("#ind_center_api_tbl tbody").html('<tr id="no_row_found"><td valign="top" colspan="8" class="dataTables_empty">मिलता-जुलता कोई रिकॉर्ड नहीं मिला</td></tr>');
                        }
                        jQuery(".date_section .loader").hide();  
                    }else{
                        jQuery('.ind-center_api_tbl tbody').html(tableData);
                        jQuery(".date_section .loader").hide();
                    }
                } 

            } 
             jQuery("#ind_center_api_tbl th.sort").each(function(){
                }) 

        },
        
        error: function() {
            jQuery(".date_section .loader").hide();
            
        },
        complete: function() {
    
        }
    });
    
}

function searchCenterAPIKey(){
   
  var input,input1,input2, input3, input4, filter,filter1,filter2, filter3, filter4, table, tr, td, td1 , td2, td3, td4, i, txtValue,txtValue1, txtValue2, txtValue3, txtValue4;
  

  input = document.getElementById("api_centername");
  input1 = document.getElementById("api_location");
  input2 = document.getElementById("api_age");
  input3 = document.getElementById("api_vaccine_type");
  input4 = document.getElementById("api_payment_type");
  filter = input.value.toUpperCase();
  filter1 = input1.value.toUpperCase();
  filter2 = input2.value.toUpperCase();
  filter3 = input3.value.toUpperCase();
  filter4 = input4.value.toUpperCase();
  //alert(filter3);
  table = document.getElementById("ind_center_api_tbl");
  tr = table.getElementsByTagName("tr");
  var noText= 0;
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    td1 = tr[i].getElementsByTagName("td")[1];
    td2 = tr[i].getElementsByTagName("td")[3];
    td3 = tr[i].getElementsByTagName("td")[2];
    td4 = tr[i].getElementsByTagName("td")[5];    
    if (td && td1 && td2 && td3 && td4) {
      txtValue = td.textContent || td.innerText;
      txtValue1 = td1.textContent || td1.innerText;
      txtValue2 = td2.textContent || td2.innerText;
      txtValue3 = td3.textContent || td3.innerText;
      txtValue4 = td4.textContent || td4.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1 && txtValue1.toUpperCase().indexOf(filter1) > -1 && txtValue2.toUpperCase().indexOf(filter2) > -1 && txtValue3.toUpperCase().indexOf(filter3) > -1 && txtValue4.toUpperCase().indexOf(filter4) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if (td && td1 && td2 && td3) {
      txtValue = td.textContent || td.innerText;
      txtValue1 = td1.textContent || td1.innerText;
      txtValue2 = td2.textContent || td2.innerText;
      txtValue3 = td3.textContent || td3.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1 && txtValue1.toUpperCase().indexOf(filter1) > -1 && txtValue2.toUpperCase().indexOf(filter2) > -1 && txtValue3.toUpperCase().indexOf(filter3) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if (td && td1 && td2 && td4) {
      txtValue = td.textContent || td.innerText;
      txtValue1 = td1.textContent || td1.innerText;
      txtValue2 = td2.textContent || td2.innerText;
      txtValue4 = td4.textContent || td4.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1 && txtValue1.toUpperCase().indexOf(filter1) > -1 && txtValue2.toUpperCase().indexOf(filter2) > -1 && txtValue4.toUpperCase().indexOf(filter4) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if (td && td1 && td4 && td3) {
      txtValue = td.textContent || td.innerText;
      txtValue1 = td1.textContent || td1.innerText;
      txtValue4 = td4.textContent || td4.innerText;
      txtValue3 = td3.textContent || td3.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1 && txtValue1.toUpperCase().indexOf(filter1) > -1 && txtValue4.toUpperCase().indexOf(filter4) > -1 && txtValue3.toUpperCase().indexOf(filter3) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if (td && td4 && td2 && td3) {
      txtValue = td.textContent || td.innerText;
      txtValue4 = td4.textContent || td4.innerText;
      txtValue2 = td2.textContent || td2.innerText;
      txtValue3 = td3.textContent || td3.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1 && txtValue4.toUpperCase().indexOf(filter4) > -1 && txtValue2.toUpperCase().indexOf(filter2) > -1 && txtValue3.toUpperCase().indexOf(filter3) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if (td4 && td1 && td2 && td3) {
      txtValue4 = td4.textContent || td4.innerText;
      txtValue1 = td1.textContent || td1.innerText;
      txtValue2 = td2.textContent || td2.innerText;
      txtValue3 = td3.textContent || td3.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1 && txtValue1.toUpperCase().indexOf(filter1) > -1 && txtValue2.toUpperCase().indexOf(filter2) > -1 && txtValue3.toUpperCase().indexOf(filter3) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if (td && td1 && td2) {
      txtValue = td.textContent || td.innerText;
      txtValue1 = td1.textContent || td1.innerText;
      txtValue2 = td2.textContent || td2.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1 && txtValue1.toUpperCase().indexOf(filter1) > -1 && txtValue2.toUpperCase().indexOf(filter2) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if (td && td1 && td3) {
      txtValue = td.textContent || td.innerText;
      txtValue1 = td1.textContent || td1.innerText;
      txtValue3 = td3.textContent || td3.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1 && txtValue1.toUpperCase().indexOf(filter1) > -1 && txtValue3.toUpperCase().indexOf(filter3) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if (td && td1 && td4) {
      txtValue = td.textContent || td.innerText;
      txtValue1 = td1.textContent || td1.innerText;
      txtValue4 = td4.textContent || td4.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1 && txtValue1.toUpperCase().indexOf(filter1) > -1 && txtValue4.toUpperCase().indexOf(filter4) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if (td && td3 && td2) {
      txtValue = td.textContent || td.innerText;
      txtValue3 = td3.textContent || td3.innerText;
      txtValue2 = td2.textContent || td2.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1 && txtValue3.toUpperCase().indexOf(filter3) > -1 && txtValue2.toUpperCase().indexOf(filter2) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if (td && td3 && td4) {
      txtValue = td.textContent || td.innerText;
      txtValue3 = td3.textContent || td3.innerText;
      txtValue4 = td4.textContent || td4.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1 && txtValue3.toUpperCase().indexOf(filter3) > -1 && txtValue4.toUpperCase().indexOf(filter4) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if (td && td4 && td2) {
      txtValue = td.textContent || td.innerText;
      txtValue4 = td4.textContent || td4.innerText;
      txtValue2 = td2.textContent || td2.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1 && txtValue4.toUpperCase().indexOf(filter4) > -1 && txtValue2.toUpperCase().indexOf(filter2) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if (td3 && td1 && td2) {
      txtValue3 = td3.textContent || td3.innerText;
      txtValue1 = td1.textContent || td1.innerText;
      txtValue2 = td2.textContent || td2.innerText;
      if (txtValue3.toUpperCase().indexOf(filter3) > -1 && txtValue1.toUpperCase().indexOf(filter1) > -1 && txtValue2.toUpperCase().indexOf(filter2) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if (td4 && td1 && td2) {
      txtValue4 = td4.textContent || td4.innerText;
      txtValue1 = td1.textContent || td1.innerText;
      txtValue2 = td2.textContent || td2.innerText;
      if (txtValue4.toUpperCase().indexOf(filter4) > -1 && txtValue1.toUpperCase().indexOf(filter1) > -1 && txtValue2.toUpperCase().indexOf(filter2) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if (td3 && td4 && td2) {
      txtValue3 = td3.textContent || td3.innerText;
      txtValue4 = td4.textContent || td4.innerText;
      txtValue2 = td2.textContent || td2.innerText;
      if (txtValue3.toUpperCase().indexOf(filter3) > -1 && txtValue4.toUpperCase().indexOf(filter4) > -1 && txtValue2.toUpperCase().indexOf(filter2) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if (td3 && td1 && td4) {
      txtValue3 = td3.textContent || td3.innerText;
      txtValue1 = td1.textContent || td1.innerText;
      txtValue4 = td4.textContent || td4.innerText;
      if (txtValue3.toUpperCase().indexOf(filter3) > -1 && txtValue1.toUpperCase().indexOf(filter1) > -1 && txtValue4.toUpperCase().indexOf(filter4) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if (td2 && td1 && td4) {
      txtValue2 = td2.textContent || td2.innerText;
      txtValue1 = td1.textContent || td1.innerText;
      txtValue4 = td4.textContent || td4.innerText;
      if (txtValue3.toUpperCase().indexOf(filter3) > -1 && txtValue1.toUpperCase().indexOf(filter1) > -1 && txtValue4.toUpperCase().indexOf(filter4) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if (td && td1 ) {
      txtValue = td.textContent || td.innerText;
      txtValue1 = td1.textContent || td1.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1 && txtValue1.toUpperCase().indexOf(filter1) > -1 ) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if (td &&  td2) {
      txtValue = td.textContent || td.innerText;
      txtValue2 = td2.textContent || td2.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1  && txtValue2.toUpperCase().indexOf(filter2) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if ( td1 && td2) {
      txtValue1 = td1.textContent || td1.innerText;
      txtValue2 = td2.textContent || td2.innerText;
      if (txtValue1.toUpperCase().indexOf(filter1) > -1 && txtValue2.toUpperCase().indexOf(filter2) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if ( td1 && td3) {
      txtValue1 = td1.textContent || td1.innerText;
      txtValue3 = td3.textContent || td3.innerText;
      if (txtValue1.toUpperCase().indexOf(filter1) > -1 && txtValue3.toUpperCase().indexOf(filter3) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if ( td3 && td2) {
      txtValue3 = td3.textContent || td3.innerText;
      txtValue2 = td2.textContent || td2.innerText;
      if (txtValue3.toUpperCase().indexOf(filter3) > -1 && txtValue2.toUpperCase().indexOf(filter2) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if ( td4 && td2) {
      txtValue4 = td4.textContent || td4.innerText;
      txtValue2 = td2.textContent || td2.innerText;
      if (txtValue4.toUpperCase().indexOf(filter4) > -1 && txtValue2.toUpperCase().indexOf(filter2) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if ( td && td3) {
      txtValue = td.textContent || td.innerText;
      txtValue3 = td3.textContent || td3.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1 && txtValue3.toUpperCase().indexOf(filter3) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if ( td4 && td3) {
      txtValue4 = td4.textContent || td4.innerText;
      txtValue3 = td3.textContent || td3.innerText;
      if (txtValue4.toUpperCase().indexOf(filter4) > -1 && txtValue3.toUpperCase().indexOf(filter3) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if ( td && td4) {
      txtValue = td.textContent || td.innerText;
      txtValue4 = td4.textContent || td4.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1 && txtValue4.toUpperCase().indexOf(filter4) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    } else if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter)) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    } else if (td1) {
      txtValue1 = td1.textContent || td1.innerText;
      if (txtValue1.toUpperCase().indexOf(filter1) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if (td2) {
      txtValue2 = td2.textContent || td2.innerText;
      if (txtValue2.toUpperCase().indexOf(filter2) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if(td3){
      txtValue3 = td3.textContent || td3.innerText;
      if (txtValue3.toUpperCase().indexOf(filter3) > -1 ) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }else if(td4){
      txtValue4 = td4.textContent || td4.innerText;
      if (txtValue4.toUpperCase().indexOf(filter4) > -1 ) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }
       
  }
  
   if(noText == 0){
      //if(jQuery("#no_row_found").html() == undefined){
         
          if(jQuery( "#lang .actv" ).html() == "English"){
                jQuery("#ind_center_api_tbl tbody").append('<tr id="no_row_found"><td valign="top" colspan="8" class="dataTables_empty">No matching records found</td></tr>');
            }else{
                jQuery("#ind_center_api_tbl tbody").append('<tr id="no_row_found"><td valign="top" colspan="8" class="dataTables_empty">मिलता-जुलता कोई रिकॉर्ड नहीं मिला</td></tr>');
               
            }
      /*}else{
            jQuery("#ind_center_api_tbl").css("display:block");
            jQuery("#no_row_found").remove();
      }*/
  }else{
      jQuery("#no_row_found").remove();
  }
}
function searchCenterAPIKey1(d){

      if(d == jQuery("#api_date").val()){
         jQuery("#api_date").val('');

      }else{
        jQuery("#api_date").val(d);
      }
     
    searchCenterAPIKey();
}
jQuery(document).ready(function(){
    jQuery(".tab_pin").hide();
    jQuery(".tab_district").show();    
    jQuery(".filter_cat").hide();
    jQuery(".date_section").hide();
    jQuery(".tab_search .dist").addClass("active");
    jQuery(".filter_cat .loader").removeClass("op");
    jQuery(".filter_cat .loader").addClass("cls");
    jQuery("#info-2 #edit-title").attr("id","edit-title2");
    jQuery("#info-4 #edit-title").attr("id","edit-title3");
    jQuery("#info-2 #edit-field-advisory-category-tid").attr("id","edit-field-advisory-category-tid2");
    jQuery("#info-2 #edit-submit-covid-states-advisory").attr("id","edit-submit-covid-states-advisory2");
    jQuery("#info-4 #edit-submit-covid-states-advisory").attr("id","edit-submit-covid-states-advisory3");
    showCenterAPITableData();
    var i = 0;
    //$( "#ind_center_api_tbl th:nth-child(3)" ).addClass( "notshort" );
    //$( "#ind_center_api_tbl th:nth-child(4)" ).addClass( "notshort" );
    $( "#ind_center_api_tbl th:nth-child(5)" ).addClass( "notshort" );
    $( "#ind_center_api_tbl th:nth-child(6)" ).addClass( "notshort" );
    $( "#ind_center_api_tbl th:nth-child(7)" ).addClass( "notshort" );
    jQuery("#ind_center_api_tbl th.sort").each(function(){

        if(i < 4 || i == 5){
           sorttable.innerSortFunction.apply(this, []); 
        }else{

        }
        i++;    
    })
    if(device == 'mobile') {
        jQuery('#_centers_list_api .ind-mp_more-btn').on('click', function(){
            jQuery('#_centers_list_api div.ind-mp_info').addClass('full-data-show');
        })
    }
})
function changeTab(tab){
    jQuery(".tab_search li").removeClass("active");
    jQuery(".filter_cat").hide();
    jQuery(".date_section").hide();
    if(tab == "pin"){
        jQuery(".tab_district").hide();
        jQuery(".tab_pin").show();        
        jQuery(".tab_search .pin").addClass("active");
        jQuery("#api_state").val('');
        jQuery("#api_district").val('');
    }else{
        jQuery(".tab_pin").hide();
        jQuery(".tab_district").show();
        jQuery(".tab_search .dist").addClass("active");
        jQuery("#api_pincode").val('');
    }
}


