using System;
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

namespace NeuroAdaptive.Networking
{
    public class BackendClient : MonoBehaviour
    {
        [SerializeField] private string backendBaseUrl = "http://127.0.0.1:8000";

        [Serializable]
        public class EEGData
        {
            public int sampling_rate_hz;
            public float signal_quality;
            public float alpha_power;
            public float beta_power;
            public float theta_power;
            public float artifact_level;
        }

        [Serializable]
        public class ActivityData
        {
            public string activity;
            public float heart_rate_bpm;
            public float speed_kmh;
            public float effort;
            public float fatigue;
        }

        [Serializable]
        public class ExperimentalStateData
        {
            public string label;
            public float confidence;
            public string coaching_message;
        }

        [Serializable]
        public class SessionSample
        {
            public EEGData eeg;
            public ActivityData activity;
            public ExperimentalStateData estimated_state;
        }

        public void RequestSample(
            Action<SessionSample> onSuccess,
            Action<string> onError = null)
        {
            StartCoroutine(RequestSampleRoutine(onSuccess, onError));
        }

        private IEnumerator RequestSampleRoutine(
            Action<SessionSample> onSuccess,
            Action<string> onError)
        {
            string url = $"{backendBaseUrl}/api/v1/session/sample";

            using (UnityWebRequest request = UnityWebRequest.Get(url))
            {
                yield return request.SendWebRequest();

                if (request.result != UnityWebRequest.Result.Success)
                {
                    string message =
                        $"Backend request failed: {request.error} ({request.responseCode})";

                    Debug.LogWarning($"[NeuroAdaptive] {message}");
                    onError?.Invoke(message);
                    yield break;
                }

                try
                {
                    SessionSample sample =
                        JsonUtility.FromJson<SessionSample>(
                            request.downloadHandler.text
                        );

                    onSuccess?.Invoke(sample);
                }
                catch (Exception exception)
                {
                    string message =
                        $"Could not parse backend response: {exception.Message}";

                    Debug.LogError($"[NeuroAdaptive] {message}");
                    onError?.Invoke(message);
                }
            }
        }
    }
}
