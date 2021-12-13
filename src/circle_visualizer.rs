use adw::prelude::*;
use async_trait::async_trait;
use gtk::{
    glib::{self, clone},
    subclass::prelude::*,
    CompositeTemplate,
};

use std::{cell::RefCell, future::Future, time::Duration};

use crate::circle::Circle;
use crate::visualizer::Visualizer;

mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate)]
    #[template(resource = "/io/github/seadve/Breathing/ui/circle-visualizer.ui")]
    pub struct CircleVisualizer {
        #[template_child]
        pub circle_1: TemplateChild<Circle>,
        #[template_child]
        pub circle_2: TemplateChild<Circle>,
        #[template_child]
        pub circle_3: TemplateChild<Circle>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for CircleVisualizer {
        const NAME: &'static str = "BtgCircleVisualizer";
        type Type = super::CircleVisualizer;
        type ParentType = gtk::Widget;

        fn class_init(klass: &mut Self::Class) {
            Self::bind_template(klass);
        }

        fn instance_init(obj: &glib::subclass::InitializingObject<Self>) {
            obj.init_template();
        }
    }

    impl ObjectImpl for CircleVisualizer {
        fn dispose(&self, obj: &Self::Type) {
            while let Some(child) = obj.first_child() {
                child.unparent();
            }
        }
    }

    impl WidgetImpl for CircleVisualizer {}
}

glib::wrapper! {
    pub struct CircleVisualizer(ObjectSubclass<imp::CircleVisualizer>)
        @extends gtk::Widget;
}

impl CircleVisualizer {
    pub fn new() -> Self {
        glib::Object::new(&[]).expect("Failed to create CircleVisualizer")
    }

    fn do_animation(
        &self,
        target: &Circle,
        is_reverse: bool,
        coefficient: f64,
        duration: Duration,
    ) -> impl Future<Output = ()> {
        let callback = adw::CallbackAnimationTarget::new(Some(Box::new(
            clone!(@weak target => move |value| {
                target.set_size((value * coefficient) as u32);
            }),
        )));

        let animation = adw::TimedAnimation::builder()
            .value_from(0.0)
            .value_to(100.0)
            .easing(adw::Easing::EaseInOutCubic)
            .target(&callback)
            .reverse(is_reverse)
            .duration(duration.as_millis() as u32)
            .widget(target)
            .build();

        let (sender, receiver) = futures_channel::oneshot::channel();
        let sender = RefCell::new(Some(sender));

        animation.connect_done(move |_| {
            sender.take().unwrap().send(()).unwrap();
        });

        animation.play();

        async move { receiver.await.unwrap() }
    }
}

#[async_trait(?Send)]
impl Visualizer for CircleVisualizer {
    async fn inhale(&self, duration: Duration) {
        let imp = imp::CircleVisualizer::from_instance(self);

        let handle_3 = self.do_animation(&imp.circle_3.get(), false, 1.5, duration);
        glib::timeout_future(Duration::from_millis(150)).await;
        let handle_2 = self.do_animation(&imp.circle_2.get(), false, 1.0, duration);
        glib::timeout_future(Duration::from_millis(75)).await;
        let handle_1 = self.do_animation(&imp.circle_1.get(), false, 0.5, duration);

        handle_1.await;
        handle_2.await;
        handle_3.await;
    }

    async fn exhale(&self, duration: Duration) {
        let imp = imp::CircleVisualizer::from_instance(self);

        let handle_1 = self.do_animation(&imp.circle_1.get(), true, 0.5, duration);
        glib::timeout_future(Duration::from_millis(75)).await;
        let handle_2 = self.do_animation(&imp.circle_2.get(), true, 1.0, duration);
        glib::timeout_future(Duration::from_millis(150)).await;
        let handle_3 = self.do_animation(&imp.circle_3.get(), true, 1.5, duration);

        handle_1.await;
        handle_2.await;
        handle_3.await;
    }
}
