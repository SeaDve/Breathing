use adw::prelude::*;
use gtk::{
    glib::{self, clone},
    subclass::prelude::*,
};
use once_cell::unsync::OnceCell;

use std::{
    cell::{Cell, RefCell},
    time::Duration,
};

use crate::visualizer::{Visualizer, VisualizerExt};

mod imp {
    use super::*;

    #[derive(Debug, Default)]
    pub struct Animator {
        pub target: OnceCell<Visualizer>,
        pub max_size: Cell<u32>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for Animator {
        const NAME: &'static str = "BtgAnimator";
        type Type = super::Animator;
        type ParentType = glib::Object;
    }

    impl ObjectImpl for Animator {
        fn properties() -> &'static [glib::ParamSpec] {
            use once_cell::sync::Lazy;
            static PROPERTIES: Lazy<Vec<glib::ParamSpec>> = Lazy::new(|| {
                vec![
                    glib::ParamSpec::new_object(
                        "target",
                        "Target",
                        "Visualizer to animate",
                        Visualizer::static_type(),
                        glib::ParamFlags::READWRITE | glib::ParamFlags::CONSTRUCT_ONLY,
                    ),
                    glib::ParamSpec::new_uint(
                        "max-size",
                        "Max size",
                        "Max size of target",
                        u32::MIN,
                        u32::MAX,
                        0,
                        glib::ParamFlags::READWRITE | glib::ParamFlags::EXPLICIT_NOTIFY,
                    ),
                ]
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
                "target" => {
                    let target = value.get().unwrap();
                    obj.set_target(target);
                }
                "max-size" => {
                    let max_size = value.get().unwrap();
                    obj.set_max_size(max_size);
                }
                _ => unimplemented!(),
            }
        }

        fn property(&self, obj: &Self::Type, _id: usize, pspec: &glib::ParamSpec) -> glib::Value {
            match pspec.name() {
                "target" => obj.target().to_value(),
                "max-size" => obj.max_size().to_value(),
                _ => unimplemented!(),
            }
        }
    }
}

glib::wrapper! {
    pub struct Animator(ObjectSubclass<imp::Animator>);
}

impl Animator {
    pub fn new(visualizer: &impl IsA<Visualizer>, max_size: u32) -> Self {
        glib::Object::new(&[]).expect("Failed to create Animator")
    }

    pub fn set_max_size(&self, max_size: u32) {
        let imp = imp::Animator::from_instance(self);
        imp.max_size.set(max_size);
        self.notify("max-size");
    }

    pub fn max_size(&self) -> u32 {
        let imp = imp::Animator::from_instance(self);
        imp.max_size.get()
    }

    pub fn target(&self) -> Visualizer {
        let imp = imp::Animator::from_instance(self);
        imp.target.get().unwrap().clone()
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

        let animation = self.build_animation(is_reverse, duration);

        animation.connect_done(move |_| {
            sender.take().unwrap().send(()).unwrap();
        });

        animation.play();

        receiver.await.unwrap();
    }

    fn set_target(&self, target: Visualizer) {
        let imp = imp::Animator::from_instance(self);
        imp.target.set(target).unwrap();
        self.notify("target");
    }

    fn build_animation(&self, is_reverse: bool, duration: Duration) -> adw::TimedAnimation {
        let callback = adw::CallbackAnimationTarget::new(Some(Box::new(
            clone!(@weak self as obj => move |value| {
                obj.target().set_size(value as u32);
            }),
        )));

        adw::TimedAnimation::builder()
            .value_from(0.0)
            .value_to(self.max_size() as f64)
            .easing(adw::Easing::EaseInOutCubic)
            .target(&callback)
            .reverse(is_reverse)
            .duration(duration.as_millis() as u32)
            .widget(&self.target())
            .build()
    }
}
