use adw::prelude::*;
use gtk::{
    glib::{self, clone},
    subclass::prelude::*,
    CompositeTemplate,
};

use std::{
    cell::{Cell, RefCell},
    time::Duration,
};

use crate::circle::Circle;

mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate)]
    #[template(resource = "/io/github/seadve/Breathing/ui/visualizer.ui")]
    pub struct Visualizer {
        #[template_child]
        pub circle: TemplateChild<Circle>,

        pub max_size: Cell<u32>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for Visualizer {
        const NAME: &'static str = "BtgVisualizer";
        type Type = super::Visualizer;
        type ParentType = gtk::Widget;

        fn class_init(klass: &mut Self::Class) {
            Self::bind_template(klass);
        }

        fn instance_init(obj: &glib::subclass::InitializingObject<Self>) {
            obj.init_template();
        }
    }

    impl ObjectImpl for Visualizer {
        fn properties() -> &'static [glib::ParamSpec] {
            use once_cell::sync::Lazy;
            static PROPERTIES: Lazy<Vec<glib::ParamSpec>> = Lazy::new(|| {
                vec![glib::ParamSpec::new_uint(
                    "max-size",
                    "Max size",
                    "Max size of Visualizer",
                    u32::MIN,
                    u32::MAX,
                    0,
                    glib::ParamFlags::READWRITE | glib::ParamFlags::EXPLICIT_NOTIFY,
                )]
            });
            PROPERTIES.as_ref()
        }

        fn set_property(
            &self,
            obj: &Self::Type,
            _id: usize,
            value: &glib::Value,
            pspec: &glib::ParamSpec,
        ) {
            match pspec.name() {
                "max-size" => {
                    let max_size = value.get().unwrap();
                    obj.set_max_size(max_size);
                }
                _ => unimplemented!(),
            }
        }

        fn property(&self, obj: &Self::Type, _id: usize, pspec: &glib::ParamSpec) -> glib::Value {
            match pspec.name() {
                "max-size" => obj.max_size().to_value(),
                _ => unimplemented!(),
            }
        }

        fn dispose(&self, obj: &Self::Type) {
            while let Some(child) = obj.first_child() {
                child.unparent();
            }
        }
    }

    impl WidgetImpl for Visualizer {}
}

glib::wrapper! {
    pub struct Visualizer(ObjectSubclass<imp::Visualizer>)
        @extends gtk::Widget;
}

impl Visualizer {
    pub fn new() -> Self {
        glib::Object::new(&[]).expect("Failed to create Visualizer")
    }

    pub fn set_max_size(&self, max_size: u32) {
        let imp = imp::Visualizer::from_instance(self);
        imp.max_size.set(max_size);
        self.notify("max-size");
    }

    pub fn max_size(&self) -> u32 {
        let imp = imp::Visualizer::from_instance(self);
        imp.max_size.get()
    }

    pub async fn expand(&self, duration: Duration) {
        let is_reverse = false;
        self.animate_inner(is_reverse, duration).await;
    }

    pub async fn shrink(&self, duration: Duration) {
        let is_reverse = true;
        self.animate_inner(is_reverse, duration).await;
    }

    async fn animate_inner(&self, is_reverse: bool, duration: Duration) {
        let (sender, receiver) = futures_channel::oneshot::channel();
        let sender = RefCell::new(Some(sender));

        let animation = self.default_animation();
        animation.set_reverse(is_reverse);
        animation.set_duration(duration.as_millis() as u32);

        animation.connect_done(move |_| {
            sender.take().unwrap().send(()).unwrap();
        });

        animation.play();

        receiver.await.unwrap();
    }

    fn animation_target(&self, value: f64) {
        log::info!("Target reached with value `{}`", value);

        let imp = imp::Visualizer::from_instance(self);
        imp.circle.set_size(value as u32);
    }

    fn default_animation(&self) -> adw::TimedAnimation {
        let imp = imp::Visualizer::from_instance(self);

        let callback = adw::CallbackAnimationTarget::new(Some(Box::new(
            clone!(@weak self as obj => move |value| {
                obj.animation_target(value);
            }),
        )));

        adw::TimedAnimation::builder()
            .widget(&imp.circle.get())
            .value_from(0.0)
            .value_to(self.max_size() as f64)
            .easing(adw::Easing::EaseInOutCubic)
            .target(&callback)
            .build()
    }
}
