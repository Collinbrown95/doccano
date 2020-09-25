import DocumentService from '@/services/document.service'
import AnnotationService from '@/services/annotation.service'

export const state = () => ({
  items: [],
  feedbackItems: [],
  selected: [],
  loading: false,
  current: 0,
  total: 0,
  totalFeedback: 0,
  searchOptions: {
    limit: 10,
    offset: 0,
    q: '',
    isChecked: '',
    filterName: ''
  }
})

export const getters = {
  isDocumentSelected(state) {
    return state.selected.length > 0
  },
  approved(state) {
    if (state.items[state.current]) {
      return state.items[state.current].annotation_approver !== null
    } else {
      return false
    }
  },
  feedback(state) {
    if (state.items[state.current]) {
      return state.items[state.current].document_feedback
    } else {
      return null
    }
  },
  currentDoc(state) {
    return state.items[state.current]
  }
}

export const mutations = {
  setCurrent(state, payload) {
    state.current = payload
  },
  setDocumentList(state, payload) {
    state.items = payload
  },
  setDocumentFeedbackList(state, payload) {
    state.feedbackItems = payload
  },
  addDocument(state, document) {
    state.items.unshift(document)
  },
  deleteDocument(state, documentId) {
    state.items = state.items.filter(item => item.id !== documentId)
  },
  updateSelected(state, selected) {
    state.selected = selected
  },
  updateDocument(state, document) {
    const item = state.items.find(item => item.id === document.id)
    Object.assign(item, document)
  },
  updateFeedback(state, payload) {
    const item = state.items.find(item => item.id === payload.document.id)
    if (item.document_feedback === null) {
      item.document_feedback = {
        text: payload.newInput
      }
    } else {
      item.document_feedback.text = payload.newInput
    }
  },
  resetSelected(state) {
    state.selected = []
  },
  setLoading(state, payload) {
    state.loading = payload
  },
  setTotalItems(state, payload) {
    state.total = payload
  },
  setTotalFeedbackItems(state, payload) {
    state.totalFeedback = payload
  },
  addAnnotation(state, payload) {
    state.items[state.current].annotations.push(payload)
  },
  deleteAnnotation(state, annotationId) {
    state.items[state.current].annotations = state.items[state.current].annotations.filter(item => item.id !== annotationId)
  },
  updateAnnotation(state, payload) {
    const item = state.items[state.current].annotations.find(item => item.id === payload.id)
    Object.assign(item, payload)
  },
  updateSearchOptions(state, payload) {
    state.searchOptions = Object.assign(state.searchOptions, payload)
  },
  initSearchOptions(state) {
    state.searchOptions = {
      limit: 10,
      offset: 0,
      q: '',
      isChecked: '',
      filterName: ''
    }
  }
}

export const actions = {
  getDocumentList({ commit, state }, payload) {
    commit('setLoading', true)
    // payload = Object.assign(payload, state.searchOptions)
    return DocumentService.getDocumentList(payload)
      .then((response) => {
        console.log(response.data.results)
        commit('setDocumentList', response.data.results)
        commit('setTotalItems', response.data.count)
      })
      .catch((error) => {
        alert(error)
      })
      .finally(() => {
        commit('setLoading', false)
      })
  },
  getDocumentFeedbackList({ commit, state }, payload) {
    commit('setLoading', true)
    return DocumentService.getDocumentFeedbackList(payload)
      .then((response) => {
        console.log('feedback list is ', response.data)
        commit('setDocumentFeedbackList', response.data.results)
        commit('setTotalFeedbackItems', response.data.count)
      })
      .catch((error) => {
        alert(error)
      })
      .finally(() => {
        commit('setLoading', false)
      })
  },
  uploadDocument({ commit, dispatch }, data) {
    commit('setLoading', true)
    const formData = new FormData()
    formData.append('file', data.file)
    formData.append('format', data.format)
    const config = {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }
    return DocumentService.uploadFile(data.projectId, formData, config)
      .then((response) => {
        dispatch('getDocumentList', data)
      })
      .finally(() => {
        commit('setLoading', false)
      })
  },
  exportDocument({ commit }, data) {
    commit('setLoading', true)
    DocumentService.exportFile(data.projectId, data.format)
      .then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'file.' + data.format)
        document.body.appendChild(link)
        link.click()
      })
      .catch((error) => {
        alert(error)
      })
      .finally(() => {
        commit('setLoading', false)
      })
  },
  updateDocument({ commit }, data) {
    DocumentService.updateDocument(data.projectId, data.id, data)
      .then((response) => {
        console.log('response data is ', response.data)
        commit('updateDocument', response.data)
      })
      .catch((error) => {
        alert(error)
      })
  },
  deleteDocument({ commit, state }, projectId) {
    for (const document of state.selected) {
      DocumentService.deleteDocument(projectId, document.id)
        .then((response) => {
          commit('deleteDocument', document.id)
        })
        .catch((error) => {
          alert(error)
        })
    }
    commit('resetSelected')
  },
  addAnnotation({ commit, state }, payload) {
    const documentId = state.items[state.current].id
    AnnotationService.addAnnotation(payload.projectId, documentId, payload)
      .then((response) => {
        commit('addAnnotation', response.data)
      })
      .catch((error) => {
        alert(error)
      })
  },
  updateAnnotation({ commit, state }, payload) {
    const documentId = state.items[state.current].id
    AnnotationService.updateAnnotation(payload.projectId, documentId, payload.annotationId, payload)
      .then((response) => {
        commit('updateAnnotation', response.data)
      })
      .catch((error) => {
        alert(error)
      })
  },
  deleteAnnotation({ commit, state }, payload) {
    const documentId = state.items[state.current].id
    AnnotationService.deleteAnnotation(payload.projectId, documentId, payload.annotationId)
      .then((response) => {
        commit('deleteAnnotation', payload.annotationId)
      })
      .catch((error) => {
        alert(error)
      })
  },
  approve({ commit, getters }, payload) {
    const documentId = getters.currentDoc.id
    const data = {
      approved: !getters.currentDoc.annotation_approver
    }
    DocumentService.approveDocument(payload.projectId, documentId, data)
      .then((response) => {
        commit('updateDocument', response.data)
      })
      .catch((error) => {
        alert(error)
      })
  },
  submitFeedback({ commit, getters }, payload) {
    const documentId = getters.currentDoc.id
    const data = {
      text: payload.text,
      document: documentId
    }
    DocumentService.submitFeedback(payload.projectId, documentId, data)
      .then((response) => {
        const data = {
          id: response.data.document,
          document_feedback: {
            text: response.data.text,
            user: response.data.username,
            document: response.data.document
          }
        }
        commit('updateDocument', data)
      })
      .catch((error) => {
        alert(error)
      })
  }
}
