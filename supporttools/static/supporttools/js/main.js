/*jslint browser: true, plusplus: true, regexp: true */
/*global $, jQuery */

$(function () {
    "use strict";

    // if mobile... handle menu button click fo
    if (window.support.is_mobile || window.support.is_tablet) {
        $('a#tool_menu_button').click(function (event) {
            event.preventDefault();
            $('#tool_menu').toggleClass('hide-div').toggleClass('show-div');
        });
    }
    // else desktop... hide the menu button and show the full menu list
    else {
        $('a#tool_menu_button').hide();
        $('#tool_menu').removeClass('hide-div');

        // get correct height for sidebar
        calculate_sidebar_height();
    }

    $.extend({
        keys: function (obj) {
            var a = [];
            $.each(obj, function (k) { a.push(k); });
            return a;
        }
    });

    function anchor(href) {
        var service = href.match(/^(\/((sws\/)?student|(pws\/)?identity)\/v[0-9]+).*/),
            url = null;

        if (service) {
            $('.default-sidelinks a').each(function () {
                var root = $(this).attr('href'),
                    offset;

                if (root) {
                    offset = root.indexOf(service[1]);
                    if (offset > 0) {
                        url = root.substr(0, offset) + href;
                        return false;
                    }
                }

                return true;
            });
        }

        return url;
    }

    function presentJSONPropertyValue($container, key, value) {
        var $a,
            href;

        if (key.toLowerCase() === 'href') {
            href = anchor(value);
            if (href) {
                $a = $('<a></a>');
                $a.attr('href', href);
                $a.html(value ? value.replace(/([&\/,])/g, '$1&#8203;') : 'NULL');
                value = $a;
            }
        } else if (key.toLowerCase() === 'name') {
            value = value ? value.replace(/([ ])/g, '&nbsp;') : 'NULL';
        } else {
            switch ($.type(value)) {
            case 'undefined':
            case 'null':
                return false;  // ignore
            case 'array':
                if (value.length === 0) {
                    return false; // ignore
                }
                /* falls through */
            case 'object':
                presentJSON($container, value);
                return true; // handled
            case 'boolean':
                value = value.toString();
                break;
            case 'string':
                if (value.length === 0) {
                    return false; // ignore
                }
                /* falls through */
            default:
                break;
            }
        }

        return value;
    }

    function presentJSON($container, json_obj) {
        var $ul = $('<ul>'),
            $li,
            $span,
            $table,
            $thead,
            $tbody,
            $tr,
            $td,
            keys,
            key,
            value,
            a_obj,
            d;

        if ($.isArray(json_obj) && json_obj.length > 0) {

            if ($.type(json_obj[0]) != 'object') {
                d = [];
                $.each(json_obj, function () {
                    value = presentJSONPropertyValue($container, '', this);
                    d.push(value);
                });

                $container.append(d.join(', '));
                return;
            } else if (json_obj.length === 1 ||
                    window.support.suppress_json_tables) {
                $.each(json_obj, function () {
                    presentJSON($container, this);
                    $container.append($('<p></p>'));
                });
                return;
            }

            // gather unique keys and non-empty, interesting columns
            d = {};
            $.each(json_obj, function () {
                a_obj = this;
                $.each($.keys(a_obj), function () {
                    value = a_obj[this];
                    if (d.hasOwnProperty(this)) {
                        if (d[this].valid) {
                            d[this].valid = !(((
                                ($.type(value) === 'string' &&
                                 $.type(d[this].last_value) === 'string') ||
                                ($.type(value) === 'number' &&
                                 $.type(d[this].last_value) === 'number')) &&
                                    value === d[this].last_value));
                        } else {
                            if (($.type(value) === 'string' &&
                                    $.type(d[this].last_value) === 'string' &&
                                    value.length && value != d[this].last_value) ||
                                ($.type(value) === 'number' &&
                                    $.type(d[this].last_value) === 'number' &&
                                    value != d[this].last_value) ||
                                        (d[this].last_value === null && value !== null)) {
                                d[this].valid = true;
                            }
                        }
                    } else {
                        d[this] = {
                            valid: !(($.type(value) === 'string' && value.length === 0) || value === null),
                            last_value: value
                        };
                    }
                });
            });

            keys = $.map(d, function (o, k) { return ((o.valid) ? k : null); }).sort(function (a, b) {
                var a_lower = a.toLowerCase(),
                    b_lower = b.toLowerCase();

                // special key sort preferences
                if (a_lower === 'href' &&
                    (b_lower === 'name' || b_lower === 'regid')) {
                    return 1;
                }

                return a - b;
            });

            $li = $('<li>');
            $table = $('<table class="sws-array table table-striped"></table>');
            $thead = $('<thead></thead>');
            $tbody = $('<tbody></tbody>');
            $tr = $('<tr></tr>');

            $.each(keys, function () {
                $tr.append('<th>' + this + '</th>');
            });

            $thead.append($tr);
            $table.append($thead);
            $.each(json_obj, function () {
                a_obj = this;
                $tr = $('<tr></tr>');
                $.each(keys, function () {
                    key = this;
                    $td = $('<td></td>');
                    if (a_obj.hasOwnProperty(key)) {
                        value = presentJSONPropertyValue($td, key, a_obj[key]);
                        if ($.type(value) !== 'boolean') {
                            $td.append(value);
                        }
                    }

                    $tr.append($td);
                });
                $tbody.append($tr);
            });

            $table.append($tbody);
            $li.append($table);
            $ul.append($li);
        } else {
            $.each(json_obj, function (k, v) {
                $li = $('<li>');
                $li.append('<span class="json-key">' + k + ' : </span>');
                value = presentJSONPropertyValue($li, k, v);
                switch (value) {
                case true:      // handled
                    break;
                case false:     // ignore
                    return true;
                default:        // display
                    $span = $('<span class="json-value"></span>');
                    $span.append(value);
                    $li.append($span);
                    break;
                }

                $ul.append($li);
            });
        }

        if ($ul.find('li').length) {
            $container.append($ul);
        }
    }

    // display digested JSON
    if (window.hasOwnProperty('restclients_json_data') &&
            window.restclients_json_data) {
        var $h1 = $('.restclients-response-content h1').detach(),
            $form = $('.restclients-response-content form').detach(),
            $tabs = $('#restclient-tabs').detach(),
            original_html = $('.restclients-response-content').html();

        $('.restclients-response-content').empty();
        $('.restclients-response-content').append($h1);
        $('.restclients-response-content').append($form);
        $tabs.appendTo('.restclients-response-content');
        $('.main-content').html(original_html);

        $('.jsonview-response').JSONView(window.restclients_json_data, { collapsed: true });

        presentJSON($('.restclients-digested-response'), window.restclients_json_data);
        $tabs.show();
        $('.table.sws-array').each(function () {
            $(this).dataTable({
                searching: false,
                paging: false,
                info: false,
                'aaSorting': [[ 0, "asc" ]],
                'bPaginate': false
            });
        });
    }
});

function calculate_sidebar_height() {
    var base_h = $(".header").height(),
        header_h = 60,
        netid_h = $(".tool-app").outerHeight(),
        footer_h = $(".footer").outerHeight(),
        diff_h = base_h - (header_h + netid_h + footer_h) - 20;

    $(".tool-list-inner").height(diff_h);
}

$(window).resize(function() {
    if (!window.support.is_mobile && !window.support.is_tablet) {
        // get correct height for sidebar
        calculate_sidebar_height();
    }
});
