use gtk::{gdk, glib, graphene, prelude::*, subclass::prelude::*, CompositeTemplate};

use once_cell::unsync::OnceCell;

use crate::animator::Animator;
use crate::circle::Circle;
use crate::visualizer::{Visualizer, VisualizerExt, VisualizerImpl};

mod imp {
    use super::*;

    #[derive(Debug, Default, CompositeTemplate)]
    #[template(resource = "/io/github/seadve/Breathing/ui/circle-visualizer.ui")]
    pub struct CircleVisualizer {
        #[template_child]
        circle: TemplateChild<Circle>,

        animator: OnceCell<Animator>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for CircleVisualizer {
        const NAME: &'static str = "NwtyCircleVisualizer";
        type Type = super::CircleVisualizer;
        type ParentType = Visualizer;
    }

    impl ObjectImpl for CircleVisualizer {
        fn constructed(&self, obj: &Self::Type) {
            let animator = Animator::new(obj, 200);
            self.animator.set(animator).unwrap();
        }

        fn dispose(&self, obj: &Self::Type) {
            while let Some(child) = obj.first_child() {
                child.unparent();
            }
        }
    }

    impl WidgetImpl for CircleVisualizer {}

    impl VisualizerImpl for CircleVisualizer {
        fn set_size(&self, obj: &Visualizer, size: u32) {
            self.circle.set_size(size);
        }
    }
}

glib::wrapper! {
    pub struct CircleVisualizer(ObjectSubclass<imp::CircleVisualizer>)
        @extends gtk::Widget, Visualizer;
}

impl CircleVisualizer {
    pub fn new() -> Self {
        glib::Object::new(&[]).expect("Failed to create CircleVisualizer")
    }
}
