use gtk::{glib, graphene, gsk, prelude::*, subclass::prelude::*};

use std::cell::Cell;

mod imp {
    use super::*;

    #[derive(Debug, Default)]
    pub struct Circle {
        pub size: Cell<u32>,
    }

    #[glib::object_subclass]
    impl ObjectSubclass for Circle {
        const NAME: &'static str = "BtgCircle";
        type Type = super::Circle;
        type ParentType = gtk::Widget;
    }

    impl ObjectImpl for Circle {
        fn properties() -> &'static [glib::ParamSpec] {
            use once_cell::sync::Lazy;
            static PROPERTIES: Lazy<Vec<glib::ParamSpec>> = Lazy::new(|| {
                vec![glib::ParamSpec::new_uint(
                    "size",
                    "Size",
                    "Size of circle",
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
                "size" => {
                    let size = value.get().unwrap();
                    obj.set_size(size);
                }
                _ => unimplemented!(),
            }
        }

        fn property(&self, obj: &Self::Type, _id: usize, pspec: &glib::ParamSpec) -> glib::Value {
            match pspec.name() {
                "size" => obj.size().to_value(),
                _ => unimplemented!(),
            }
        }
    }

    impl WidgetImpl for Circle {
        fn snapshot(&self, obj: &Self::Type, snapshot: &gtk::Snapshot) {
            obj.on_snapshot(snapshot);
        }

        fn measure(
            &self,
            obj: &Self::Type,
            orientation: gtk::Orientation,
            _for_size: i32,
        ) -> (i32, i32, i32, i32) {
            let widget_size = if orientation == gtk::Orientation::Horizontal {
                obj.width()
            } else {
                obj.height()
            };

            (widget_size, widget_size, -1, -1)
        }
    }
}

glib::wrapper! {
    pub struct Circle(ObjectSubclass<imp::Circle>)
        @extends gtk::Widget;
}

impl Circle {
    pub fn new() -> Self {
        glib::Object::new(&[]).expect("Failed to create Circle")
    }

    pub fn set_size(&self, size: u32) {
        let imp = imp::Circle::from_instance(self);
        imp.size.set(size);
        self.notify("size");

        self.queue_draw();
        self.queue_resize();
    }

    pub fn size(&self) -> u32 {
        let imp = imp::Circle::from_instance(self);
        imp.size.get()
    }

    fn on_snapshot(&self, snapshot: &gtk::Snapshot) {
        let size = self.size() as f32;

        let center_widget_width = self.width() as f32 / 2.0;
        let center_widget_height = self.height() as f32 / 2.0;

        let radius = size as f32 / 2.0;
        let bounds = graphene::Rect::new(
            center_widget_width - radius,
            center_widget_height - radius,
            size,
            size,
        );
        let circle = gsk::RoundedRect::from_rect(bounds.clone(), radius);

        let color = self.style_context().color();

        snapshot.push_rounded_clip(&circle);
        snapshot.append_color(&color, &bounds);
        snapshot.pop();
    }
}
