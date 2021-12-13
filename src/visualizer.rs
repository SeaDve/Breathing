use async_trait::async_trait;

use std::time::Duration;

#[async_trait(?Send)]
pub trait Visualizer {
    async fn inhale(&self, duration: Duration);
    async fn exhale(&self, duration: Duration);
}
