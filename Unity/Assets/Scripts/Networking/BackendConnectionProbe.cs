using UnityEngine;

namespace NeuroAdaptive.Networking
{
    public class BackendConnectionProbe : MonoBehaviour
    {
        [SerializeField] private BackendClient backendClient;
        [SerializeField] private float firstRequestDelay = 1.5f;

        private void Start()
        {
            Invoke(nameof(RequestSample), firstRequestDelay);
        }

        private void RequestSample()
        {
            if (backendClient == null)
            {
                Debug.LogWarning(
                    "[NeuroAdaptive] Assign BackendClient to BackendConnectionProbe."
                );
                return;
            }

            backendClient.RequestSample(
                sample =>
                {
                    Debug.Log(
                        "[NeuroAdaptive] SAMPLE RECEIVED\n" +
                        $"State: {sample.estimated_state.label}\n" +
                        $"Confidence: {sample.estimated_state.confidence}\n" +
                        $"Heart Rate: {sample.activity.heart_rate_bpm} BPM\n" +
                        $"Alpha Power: {sample.eeg.alpha_power}"
                    );
                },
                error =>
                {
                    Debug.LogWarning(
                        $"[NeuroAdaptive] Sample request error: {error}"
                    );
                }
            );
        }
    }
}
