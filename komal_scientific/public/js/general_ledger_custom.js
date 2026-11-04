frappe.provide("komal_scientific");

komal_scientific.add_columnar_switch_button = function (report) {
	if (!report || !report.page) return;

	// Prevent duplicate buttons
	if (report.page.inner_toolbar && $(report.page.inner_toolbar).find(".btn-switch-to-columnar").length) {
		return;
	}

	let $btn = report.page.add_inner_button(__("General Ledger - Columnar"), function () {
		let filters = report.get_values() || {};
	

		frappe.set_route("query-report", "General Ledger - Columnar", {
			company: filters.company,
			from_date: filters.from_date,
			to_date: filters.to_date,
			account: filters.account,
			
		});
	});

	if ($btn) {
		$btn.addClass("btn-switch-to-columnar");
	}
};

komal_scientific.setup_gl_switch_hook = function () {
	if (frappe.views && frappe.views.QueryReport && !frappe.views.QueryReport.prototype._has_columnar_switch_hook) {
		frappe.views.QueryReport.prototype._has_columnar_switch_hook = true;
		const original_refresh_report = frappe.views.QueryReport.prototype.refresh_report;

		frappe.views.QueryReport.prototype.refresh_report = function (route_options) {
			let res = original_refresh_report.call(this, route_options);
			if (res && res.then) {
				return res.then(() => {
					if (this.report_name === "General Ledger") {
						komal_scientific.add_columnar_switch_button(this);
					}
				});
			} else {
				if (this.report_name === "General Ledger") {
					komal_scientific.add_columnar_switch_button(this);
				}
				return res;
			}
		};
	}
};

$(document).on("app_ready", function () {
	komal_scientific.setup_gl_switch_hook();
});

// Also check and attach on route changes
frappe.router.on("change", () => {
	komal_scientific.setup_gl_switch_hook();
	let route = frappe.get_route();
	if (route && route[0] === "query-report" && route[1] === "General Ledger") {
		frappe.after_ajax(() => {
			if (frappe.query_report && frappe.query_report.report_name === "General Ledger") {
				komal_scientific.add_columnar_switch_button(frappe.query_report);
			}
		});
	}
});
