
var feedPath = '';

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

        .ind-mp_tbl {
            width: 100%; margin-top:0px;
        }

        .ind-mp_tbl thead {
            width: 100%;
        }

        .ind-mp_tbl th:nth-of-type(1) {
            background-color: rgba(234, 234, 234, .38);
            color: #4C4C4C;
            border-right: solid 1px #fff;
        }

        .ind-mp_tbl th:nth-of-type(2) {
            background: #d3a70f; /* Old browsers */
background: -moz-linear-gradient(top,  #d3a70f 0%, #f6d04a 100%); /* FF3.6-15 */
background: -webkit-linear-gradient(top,  #d3a70f 0%,#f6d04a 100%); /* Chrome10-25,Safari5.1-6 */
background: linear-gradient(to bottom,  #d3a70f 0%,#f6d04a 100%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#d3a70f', endColorstr='#f6d04a',GradientType=0 ); /* IE6-9 */
            color: #582801;
            border-right: solid 1px #fff;
        }

        .ind-mp_tbl th:nth-of-type(3),.ind-mp_tbl th:nth-of-type(6) {
            background: #a5c9fd; /* Old browsers */
background: -moz-linear-gradient(top,  #a5c9fd 0%, #bde5fc 100%); /* FF3.6-15 */
background: -webkit-linear-gradient(top,  #a5c9fd 0%,#bde5fc 100%); /* Chrome10-25,Safari5.1-6 */
background: linear-gradient(to bottom,  #a5c9fd 0%,#bde5fc 100%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#a5c9fd', endColorstr='#bde5fc',GradientType=0 ); /* IE6-9 */

            color: #002c57;
            border-right: solid 1px #fff;
        }

        .ind-mp_tbl th:nth-of-type(4),.ind-mp_tbl th:nth-of-type(7) {
           background: #9be89c; /* Old browsers */
background: -moz-linear-gradient(top,  #9be89c 0%, #cdf97d 100%); /* FF3.6-15 */
background: -webkit-linear-gradient(top,  #9be89c 0%,#cdf97d 100%); /* Chrome10-25,Safari5.1-6 */
background: linear-gradient(to bottom,  #9be89c 0%,#cdf97d 100%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#9be89c', endColorstr='#cdf97d',GradientType=0 ); /* IE6-9 */
            color: #005c25;
            border-right: solid 1px #fff;
        }

        .ind-mp_tbl th:nth-of-type(5),.ind-mp_tbl th:nth-of-type(8) {
            background: #fe8683; /* Old browsers */
background: -moz-linear-gradient(top,  #fe8683 0%, #ff9d9b 100%); /* FF3.6-15 */
background: -webkit-linear-gradient(top,  #fe8683 0%,#ff9d9b 100%); /* Chrome10-25,Safari5.1-6 */
background: linear-gradient(to bottom,  #fe8683 0%,#ff9d9b 100%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#fe8683', endColorstr='#ff9d9b',GradientType=0 ); /* IE6-9 */
            color: #5a0401;
        }
        .ind-mp_tbl th:nth-of-type(5){border-right: solid 1px #fff;}

        .ind-mp_tbl td:nth-of-type(1) {
            color: #6A6A6A;
        }

        .ind-mp_tbl td:nth-of-type(2) {
            color: #582801;
        }

        .ind-mp_tbl td:nth-of-type(3),.ind-mp_tbl td:nth-of-type(6) {
            color: #002c57;
        }

        .ind-mp_tbl td:nth-of-type(4),.ind-mp_tbl td:nth-of-type(7) {
            color: #005c25;
        }

        .ind-mp_tbl td:nth-of-type(5),.ind-mp_tbl td:nth-of-type(8) {
            color: #5a0401;
        }
        .ind-mp_tbl td:nth-of-type(4) .data-up{background: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAOCAYAAAAWo42rAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyBpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEzNDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNSBXaW5kb3dzIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOkQ2REMwOUJGREUyQTExRUFBNkVBRDlDMjI1NzEyNUVBIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOkQ2REMwOUMwREUyQTExRUFBNkVBRDlDMjI1NzEyNUVBIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6RDZEQzA5QkRERTJBMTFFQUE2RUFEOUMyMjU3MTI1RUEiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6RDZEQzA5QkVERTJBMTFFQUE2RUFEOUMyMjU3MTI1RUEiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz7NOUITAAAA7klEQVR42mL4//8/AwzzzkxwBOJ8ZDEYZgQRIMA3K5EdSC0DYicgtvyUNv8GAxJgQmLHAbEfEAsAcTdQIxeGQqCgNpBqBGIWqLgPEKcgK2QEuokDSK8BYm8GVPAMiH2BTjgHMzEfiyIQkII6QRCmMBqIvwPxLyRFv4H4AxBbA7EnTKEDEIsBcRmSwodAbAsV3wR2I1LwgHTvAWKQm78CcQDQfXuwBQ/I0QegbG4gDsYajkDdIHe2A/EbqFA80BY3bCaCFB8CUklAfA+IOYF4ElCxLoobkQFQUgNIpULxKyAuwaoQSYMrkAoFGQgQYACL/VkWKlnALQAAAABJRU5ErkJggg==') left center no-repeat; color: #4F9A0B; background-size: auto 11px;}


        .ind-mp_tbl tr {
            width: 100%;
            white-space: nowrap;
        }

        .ind-mp_tbl th:nth-of-type(1),
        .ind-mp_tbl td:nth-of-type(1) {
            width: 30%;
            text-align: left;
            white-space: normal; 
        }

        .ind-mp_tbl th:nth-of-type(2),
        .ind-mp_tbl td:nth-of-type(2) {
            width: 15%;
        }

        .ind-mp_tbl th:nth-of-type(3),
        .ind-mp_tbl td:nth-of-type(3) {
            width: 15%;
        }

        .ind-mp_tbl th:nth-of-type(4),
        .ind-mp_tbl td:nth-of-type(4) {
            width: 15%;
        }

        .ind-mp_tbl th:nth-of-type(5),
        .ind-mp_tbl td:nth-of-type(5) {
            width: 15%;
            min-width: 85px; 
        }


        .ind-mp_tbl tbody {
            width: 100%;
        }

        .ind-mp_tbl tbody tr {
           cursor: pointer;
           background:none;
        }
        
        .ind-mp_tbl td, .ind-mp_tbl th {
          border: 1px solid #ddd;
          cursor:default;
        }
        .ind_mp_tbl tr th{cursor:pointer;}
        .ind-mp_tbl tr:nth-child(even){background-color: #f2f2f2;}
        
        .ind-mp_tbl tbody tr:hover {background-color: #ddd;}
        .ind-mp_tbl th,
        .ind-mp_tbl td {
            padding: 10px;
            font-size: 1.167em;
            color: #706A6C;
            font-weight: 500;
            text-align: center;
            position: relative;
            text-transform: uppercase;
            min-width: 110px;
            letter-spacing: -0.5px;
        }

        .ind-mp_tbl th {
            font-weight: 900; cursor:pointer
        }

        .ind-mp_tbl td{ font-size: 1.167em; text-transform: capitalize;}
        

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
            font-size: 0.857em;
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
            font-size: 0.857em;
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
            font-size:0.857em;
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
            .ind-mp_tbl th, .ind-mp_tbl td { min-width: 120px; }
            .ind-mp_tbl {
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
            .full-data-show .ind-mp_tbl {
                height: auto;
            }
}
`+appsCss+`
</style>`;

if(hidetable == 1) {
}
function showTableData(){
    var addHtml = `<div class="ind-mp_data">
            <div class="ind-mp_info">
                <table class="ind-mp_tbl sortable" id="ind_mp_tbl">
                    <thead>
                        <tr>
                            <th>State/UTs</th>
                            <th class="`+((device=='desktop' || device=='mobile' || device=='apps')?'sort ':'')+`sort">Total Cases</th>
                            <th>Active</th>                         
                            <th>Discharged</th>                         
                            <th>Deaths</th>
                            <th>Active Ratio</th>
                            <th>Discharge Ratio</th>
                            <th>Death Ratio</th>
                        </tr>
                    </thead><tbody></tbody>
                </table>
                `+(device=='mobile'?'<div class="ind-mp_more"><a href="javascript:void(0);" class="ind-mp_more-btn">Show More</a></div>':'')+`
            </div>`; 
    if(stateName == "states_name_hi"){
        addHtml = `<div class="ind-mp_data">
            <div class="ind-mp_info">
                <table class="ind-mp_tbl sortable" id="ind_mp_tbl">
                    <thead>
                        <tr>
                            <th>राज्य/ संघ राज्य</th>
                            <th class="`+((device=='desktop' || device=='mobile' || device=='apps')?'sort ':'')+`sort">कुल मामले</th>
                            <th>सक्रिय मामले</th>                           
                            <th>स्वस्थ हुए</th>                         
                            <th>मृत्यु</th>
                            <th>सक्रिय अनुपात</th>
                            <th>स्वस्थ अनुपात</th>
                            <th>मृत्यु अनुपात</th>
                        </tr>
                    </thead><tbody></tbody>
                </table>
                `+(device=='mobile'?'<div class="ind-mp_more"><a href="javascript:void(0);" class="ind-mp_more-btn">Show More</a></div>':'')+`
            </div>`;
    }
jQuery('#_indiatable').html(styleCss+addHtml);
    var gatData =  '/sites/default/files/covid/covid_state_counts_ver1.json';
    var tableData = '';
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
            
            var a = stateJsonData;
            for(var k = 0; k < stateJsonData.length; k++){
                var j = stateJsonData[k];
                var activeRation = 0;
                var dischargedRation = 0;
                var deathRation = 0;
                if(parseInt(response['Total Confirmed cases'][j]) == 0){
                    activeRation = 0;
                    dischargedRation = 0;
                    deathRation = 0;
                } else{
                    
                    if(parseFloat(parseInt(response['Active'][j])) == 0){
                        activeRation = 0;
                    }else{
                        activeRation = parseFloat(parseInt(response['Active'][j])*100/parseInt(response['Total Confirmed cases'][j])).toFixed(2);
                    }
                    if(parseFloat(parseInt(response['Cured\/Discharged\/Migrated'][j])) == 0){
                        dischargedRation = 0;
                    }else{
                        dischargedRation = parseFloat(parseInt(response['Cured\/Discharged\/Migrated'][j])*100/parseInt(response['Total Confirmed cases'][j])).toFixed(2);
                    }
                    if(parseFloat(parseInt(response['Death'][j])) == 0){
                        deathRation = 0;
                    }else{
                        deathRation = parseFloat(parseInt(response['Death'][j])*100/parseInt(response['Total Confirmed cases'][j])).toFixed(2);
                    }
                    
                }
                 tableData += '<tr><td>'+response[stateName][j]+'</td><td><p class="mid-wrap">'+parseInt(response['Total Confirmed cases'][j]).toLocaleString('en-in', { timeZone: 'UTC' })+(response['diff_confirmed_covid_cases'][j] != 0?'<span class="'+((response['diff_confirmed_covid_cases'][j] > 0)?'data-up':'data-down')+'">'+Math.abs(response['diff_confirmed_covid_cases'][j]).toLocaleString('en-in', { timeZone: 'UTC' })+'</span>':'')+'</p></td><td><p class="mid-wrap">'+parseInt(response['Active'][j]).toLocaleString('en-in', { timeZone: 'UTC' })+(response['diff_active_covid_cases'][j] != 0?'<span class="'+((response['diff_active_covid_cases'][j] > 0)?'data-up':'data-down')+'">'+Math.abs(response['diff_active_covid_cases'][j]).toLocaleString('en-in', { timeZone: 'UTC' })+'</span>':'')+'</p></td><td><p class="mid-wrap">'+parseInt(response['Cured\/Discharged\/Migrated'][j]).toLocaleString('en-in', { timeZone: 'UTC' })+(response['diff_cured_discharged'][j] != 0?'<span class="'+((response['diff_cured_discharged'][j] > 0)?'data-up':'data-down')+'">'+Math.abs(response['diff_cured_discharged'][j]).toLocaleString('en-in', { timeZone: 'UTC' })+'</span>':'')+'</p></td><td><p class="mid-wrap">'+parseInt(response['Death'][j]).toLocaleString('en-in', { timeZone: 'UTC' })+(response['diff_death'][j] != 0?'<span class="'+((response['diff_death'][j] > 0)?'data-up':'data-down')+'">'+Math.abs(response['diff_death'][j]).toLocaleString('en-in', { timeZone: 'UTC' })+'</span>':'')+'</p></td><td><p class="mid-wrap mid-wrap1">'+activeRation+'%</p></td><td><p class="mid-wrap mid-wrap1">'+dischargedRation+'%</p></td><td><p class="mid-wrap mid-wrap1">'+deathRation+'%</p></td></tr>';
                
                if(tableData != '' && hidetable != 1){
                    jQuery('.ind-mp_tbl tbody').html(tableData);
                }
            }
          
            
        },
        error: function() {

        },
        complete: function() {

        }
    });

}



function searchKey() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("ind_mp_tbl");
  tr = table.getElementsByTagName("tr");
  var noText= 0;
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
        noText++;
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
   if(noText == 0){
      if(jQuery("#no_row_found").html() == undefined){
          jQuery("#ind_mp_tbl tbody").append('<tr id="no_row_found"><td valign="top" colspan="8" class="dataTables_empty">No matching records found</td></tr>');
      }else{
            jQuery("#ind_mp_tbl").css("display:block");
      }
  }else{
      jQuery("#no_row_found").remove();
  }
}


jQuery(document).ready(function(){
    showTableData();
    jQuery("#_indiatable th.sort").each(function(){
    })
    if(device == 'mobile') {
        jQuery('#_indiatable .ind-mp_more-btn').on('click', function(){
            jQuery('#_indiatable div.ind-mp_info').addClass('full-data-show');
        })
    }
})

function addCommas(nStr)
{
    nStr += '';
    x = nStr.split('.');
    x1 = x[0];
    x2 = x.length > 1 ? '.' + x[1] : '';
    var rgx = /(\d+)(\d{3})/;
    while (rgx.test(x1)) {
        x1 = x1.replace(rgx, '$1' + ',' + '$2');
    }
    return x1 + x2;
}

