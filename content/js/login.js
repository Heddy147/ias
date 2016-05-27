var LITAPP = {};

LITAPP.Application_cl = Class.create({
	initialize: function () {
		var self = this;
		this.rest = new Rest(this);

		LITAPP.es_o.subscribe_px(this, 'app');
	},
	notify_px: function (self_opl, message_spl, data_apl) {
		switch (message_spl) {
			case 'app':
				switch (data_apl[0]) {
					case 'init':
						LITAPP.tm_o = new TELIB.TemplateManager_cl();
						break;
					case 'templates.loaded':
						self_opl.render_px('guest_login', {});
						break;
					default:
						console.warning('[Application_cl] unbekannte app-Notification: '+data_apl[0]);
						break;
				}
				break;
			default:
				console.warning('[Application_cl] unbekannte Notification: '+message_spl);
				break;
		}
	},
	render_px: function(template_name, data) {
		var self = this;

		$('#content').html(LITAPP.tm_o.execute_px(template_name + '.html', data));

		$('button:not([type="submit"]), .function').click(function() {
			var action = $(this).data('action');
			if($(this).is('.function')) {
				action = 'function';
			}

			switch(action) {
				case 'page.switch':
					var templateName = $(this).data('template-name');
					self.render_px(templateName);
					break;
				case 'function':
					var functionName = $(this).data('function');
					eval("self." + functionName + "(this);");
					break;
				default:
					console.log("Action unbekannt: " + action);
					break;
			}
		});

		if ($('form#login').length > 0) {
			$('form#login').submit(function(e) {
				e.preventDefault();
				var values = {};
				$(this).find('input').each(function() {
					values[$(this).attr('name')] = $(this).val();
				});
				self.rest.doLogin(values);
			});
		}

		if ($('form#registrieren').length > 0) {
			$('form#registrieren').submit(function(e) {
				e.preventDefault();
				var values = {};
				$(this).find('input').each(function() {
					values[$(this).attr('name')] = $(this).val();
				});
				self.rest.doRegister(values);
			});
		}
	},

	setCookie: function(cname, cvalue) {
		var d = new Date();
		d.setTime(d.getTime() + 60*60*1000);
		var expires = "expires=" + d.toUTCString();

		document.cookie = cname + "=" + cvalue + "; " + expires;
	},
	getCookie: function(cname) {
		var name = cname + "=";
		var ca = document.cookie.split(';');
		for(var i=0; i<ca.length; i++) {
			var c = ca[i];
			while(c.charAt(0) == '' && c != '') {
				c = c.substring(1);
			}
			if(c.indexOf(name) == 0) {
				return c.substring(name.length, c.length);
			}
		}
		return null;
	}
});

$(document).ready(function(){
	LITAPP.es_o  = new EventService_cl();
	LITAPP.app_o = new LITAPP.Application_cl();

	LITAPP.es_o.publish_px('app', ['init', null]);

});
// EOF