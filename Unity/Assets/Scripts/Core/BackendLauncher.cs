using System.Collections;
using System.Diagnostics;
using System.IO;
using UnityEngine;
using UnityEngine.Networking;
using Debug = UnityEngine.Debug;

namespace NeuroAdaptive.Core
{
    public class BackendLauncher : MonoBehaviour
    {
        [Header("Backend")]
        [SerializeField] private string backendExecutableName = "NeuroAdaptiveBackend.exe";
        [SerializeField] private string backendRelativeFolder = "Backend";
        [SerializeField] private int backendPort = 8000;

        [Header("Development")]
        [SerializeField] private bool autoLaunchBackendInEditor = false;

        [Header("Timing")]
        [SerializeField] private float healthCheckTimeoutSeconds = 12f;
        [SerializeField] private float healthCheckIntervalSeconds = 0.5f;

        private Process backendProcess;

        public bool IsBackendOnline { get; private set; }

        private string HealthUrl => $"http://127.0.0.1:{backendPort}/health";

        private void Start()
        {
            StartCoroutine(InitializeBackend());
        }

        private IEnumerator InitializeBackend()
        {
#if UNITY_EDITOR
            if (!autoLaunchBackendInEditor)
            {
                Debug.Log("[NeuroAdaptive] Editor mode: backend auto-launch disabled.");
                yield return WaitForBackend();
                yield break;
            }
#endif

            LaunchBackendExecutable();
            yield return WaitForBackend();
        }

        private void LaunchBackendExecutable()
        {
            string executablePath = Path.Combine(
                Application.streamingAssetsPath,
                backendRelativeFolder,
                backendExecutableName
            );

            if (!File.Exists(executablePath))
            {
                Debug.LogWarning(
                    $"[NeuroAdaptive] Backend executable not found at: {executablePath}. " +
                    "This is expected before final standalone packaging."
                );
                return;
            }

            try
            {
                ProcessStartInfo startInfo = new ProcessStartInfo
                {
                    FileName = executablePath,
                    WorkingDirectory = Path.GetDirectoryName(executablePath),
                    UseShellExecute = false,
                    CreateNoWindow = true,
                };

                backendProcess = Process.Start(startInfo);
                Debug.Log("[NeuroAdaptive] Backend process launch requested.");
            }
            catch (System.Exception exception)
            {
                Debug.LogError(
                    $"[NeuroAdaptive] Failed to launch backend: {exception.Message}"
                );
            }
        }

        private IEnumerator WaitForBackend()
        {
            float elapsed = 0f;

            while (elapsed < healthCheckTimeoutSeconds)
            {
                using (UnityWebRequest request = UnityWebRequest.Get(HealthUrl))
                {
                    request.timeout = Mathf.CeilToInt(healthCheckIntervalSeconds + 2f);

                    yield return request.SendWebRequest();

                    if (request.result == UnityWebRequest.Result.Success)
                    {
                        IsBackendOnline = true;

                        Debug.Log(
                            $"[NeuroAdaptive] BACKEND ONLINE -> {request.downloadHandler.text}"
                        );

                        yield break;
                    }
                }

                elapsed += healthCheckIntervalSeconds;
                yield return new WaitForSeconds(healthCheckIntervalSeconds);
            }

            IsBackendOnline = false;

            Debug.LogWarning(
                "[NeuroAdaptive] Backend health check timed out. " +
                "Backend features are currently unavailable."
            );
        }

        private void OnApplicationQuit()
        {
            try
            {
                if (backendProcess != null && !backendProcess.HasExited)
                {
                    backendProcess.Kill();
                    backendProcess.Dispose();
                }
            }
            catch
            {
            }
        }
    }
}
