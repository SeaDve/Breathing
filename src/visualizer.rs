use adw::prelude::*;
use gtk::{glib, subclass::prelude::*};

use std::cell::Cell;

mod imp {
    use super::*;

    pub type VisualizerInstance = super::Visualizer;

    #[repr(C)]
    pub struct VisualizerClass {
        pub parent_class: gtk::ffi::GtkWidgetClass,
        pub set_size: fn(&VisualizerInstance, size: u32),
    }

    unsafe impl ClassStruct for VisualizerClass {
        type Type = Visualizer;
    }

    #[derive(Debug, Default)]
    pub struct Visualizer {
        pub size: Cell<u32>,
    }

    fn set_size_default_trampoline(this: &VisualizerInstance, size: u32) {
        Visualizer::from_instance(this).set_size(this, size)
    }

    pub(super) fn visualizer_set_size(this: &VisualizerInstance, size: u32) {
        let klass = this.class();
        (klass.as_ref().set_size)(this, size)
    }

    impl Visualizer {
        fn set_size(&self, obj: &VisualizerInstance, size: u32) {
            let imp = imp::Visualizer::from_instance(obj.as_ref());
            imp.size.set(size);
            obj.notify("size");
        }
    }

    #[glib::object_subclass]
    impl ObjectSubclass for Visualizer {
        const NAME: &'static str = "BtgVisualizer";
        type Type = super::Visualizer;
        type ParentType = gtk::Widget;
        type Class = VisualizerClass;

        fn class_init(klass: &mut Self::Class) {
            klass.set_size = set_size_default_trampoline;
        }
    }

    impl ObjectImpl for Visualizer {
        fn properties() -> &'static [glib::ParamSpec] {
            use once_cell::sync::Lazy;
            static PROPERTIES: Lazy<Vec<glib::ParamSpec>> = Lazy::new(|| {
                vec![glib::ParamSpec::new_uint(
                    "size",
                    "Size",
                    "Current size",
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
                "size" => VisualizerExt::size(obj).to_value(),
                _ => unimplemented!(),
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

    // FIXME Implement this as an interface
    pub fn inhale(&self) {}

    pub fn exhale(&self) {}
}

impl Default for Visualizer {
    fn default() -> Self {
        Self::new()
    }
}

pub trait VisualizerExt {
    fn set_size(&self, size: u32);
    fn size(&self) -> u32;
}

impl<O: IsA<Visualizer>> VisualizerExt for O {
    fn set_size(&self, size: u32) {
        imp::visualizer_set_size(self.upcast_ref::<Visualizer>(), size)
    }

    fn size(&self) -> u32 {
        let imp = imp::Visualizer::from_instance(self.as_ref());
        imp.size.get()
    }
}

pub trait VisualizerImpl: ObjectImpl + 'static {
    fn set_size(&self, obj: &Visualizer, size: u32) {
        self.parent_set_size(obj, size)
    }
}

pub trait VisualizerImplExt: ObjectSubclass {
    fn parent_set_size(&self, obj: &Visualizer, size: u32);
}

impl<T: VisualizerImpl> VisualizerImplExt for T {
    fn parent_set_size(&self, obj: &Visualizer, size: u32) {
        unsafe {
            let data = Self::type_data();
            let parent_class = &*(data.as_ref().parent_class() as *mut imp::VisualizerClass);
            (parent_class.set_size)(obj, size)
        }
    }
}

unsafe impl<T: VisualizerImpl> IsSubclassable<T> for Visualizer {
    fn class_init(class: &mut glib::Class<Self>) {
        <glib::Object as IsSubclassable<T>>::class_init(class.upcast_ref_mut());

        let klass = class.as_mut();
        klass.set_size = set_size_trampoline::<T>;
    }

    fn instance_init(instance: &mut glib::subclass::InitializingObject<T>) {
        <glib::Object as IsSubclassable<T>>::instance_init(instance);
    }
}

fn set_size_trampoline<T>(this: &Visualizer, size: u32)
where
    T: ObjectSubclass + VisualizerImpl,
{
    let imp = T::from_instance(this.dynamic_cast_ref::<T::Type>().unwrap());
    imp.set_size(this, size)
}
