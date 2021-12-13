use adw::subclass::prelude::*;
use gtk::{
    gio,
    glib::{self, clone},
    prelude::*,
    subclass::prelude::*,
    CompositeTemplate,
};

use std::time::Duration;

use crate::circle_visualizer::CircleVisualizer;
use crate::{config::PROFILE, visualizer::Visualizer, Application};

mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate)]
    #[template(resource = "/io/github/seadve/Breathing/ui/window.ui")]
    pub struct Window {
        #[template_child]
        pub visualizer: TemplateChild<CircleVisualizer>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for Window {
        const NAME: &'static str = "BtgWindow";
        type Type = super::Window;
        type ParentType = adw::ApplicationWindow;

        fn class_init(klass: &mut Self::Class) {
            Self::bind_template(klass);

            klass.install_action("window.inhale", None, move |obj, _, _| {
                let ctx = glib::MainContext::default();
                ctx.spawn_local(clone!(@weak obj => async move {
                    let imp = imp::Window::from_instance(&obj);
                    imp.visualizer.inhale(Duration::from_secs(2)).await;
                    log::info!("Inhale done");
                }));
            });

            klass.install_action("window.exhale", None, move |obj, _, _| {
                let ctx = glib::MainContext::default();
                ctx.spawn_local(clone!(@weak obj => async move {
                    let imp = imp::Window::from_instance(&obj);
                    imp.visualizer.exhale(Duration::from_secs(6)).await;
                    log::info!("Exhale done");
                }));
            });
        }

        fn instance_init(obj: &glib::subclass::InitializingObject<Self>) {
            obj.init_template();
        }
    }

    impl ObjectImpl for Window {
        fn constructed(&self, obj: &Self::Type) {
            self.parent_constructed(obj);

            if PROFILE == "Devel" {
                obj.add_css_class("devel");
            }

            obj.load_window_size();
        }
    }

    impl WidgetImpl for Window {}
    impl WindowImpl for Window {
        fn close_request(&self, window: &Self::Type) -> gtk::Inhibit {
            if let Err(err) = window.save_window_size() {
                log::warn!("Failed to save window state, {}", &err);
            }

            self.parent_close_request(window)
        }
    }

    impl ApplicationWindowImpl for Window {}
    impl AdwApplicationWindowImpl for Window {}
}

glib::wrapper! {
    pub struct Window(ObjectSubclass<imp::Window>)
        @extends gtk::Widget, gtk::Window, gtk::ApplicationWindow, adw::ApplicationWindow,
        @implements gio::ActionMap, gio::ActionGroup;
}

impl Window {
    pub fn new(app: &Application) -> Self {
        glib::Object::new(&[("application", app)]).expect("Failed to create Window")
    }

    fn save_window_size(&self) -> Result<(), glib::BoolError> {
        let settings = Application::default().settings();

        let (width, height) = self.default_size();

        settings.set_int("window-width", width)?;
        settings.set_int("window-height", height)?;

        settings.set_boolean("is-maximized", self.is_maximized())?;

        Ok(())
    }

    fn load_window_size(&self) {
        let settings = Application::default().settings();

        let width = settings.int("window-width");
        let height = settings.int("window-height");
        let is_maximized = settings.boolean("is-maximized");

        self.set_default_size(width, height);

        if is_maximized {
            self.maximize();
        }
    }
}
