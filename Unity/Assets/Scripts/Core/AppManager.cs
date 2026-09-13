using UnityEngine;

namespace NeuroAdaptive.Core
{
    public class AppManager : MonoBehaviour
    {
        public static AppManager Instance { get; private set; }

        [Header("Application")]
        [SerializeField] private bool persistAcrossScenes = true;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;

            if (persistAcrossScenes)
            {
                DontDestroyOnLoad(gameObject);
            }

            Debug.Log("[NeuroAdaptive] Application manager initialized.");
        }
    }
}
